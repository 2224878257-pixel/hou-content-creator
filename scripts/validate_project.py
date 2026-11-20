#!/usr/bin/env python3
"""Validate repository structure, references, metadata, and release inputs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "hou-content-creator"
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", text, re.S)
    if not match:
        fail(f"Missing or invalid YAML frontmatter: {path.relative_to(ROOT)}")
        return {}, text
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data, match.group(2)


def validate_skill() -> None:
    skill_md = SKILL / "SKILL.md"
    if not skill_md.is_file():
        fail("skills/hou-content-creator/SKILL.md is missing")
        return
    metadata, body = parse_frontmatter(skill_md)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != SKILL.name:
        fail(f"Skill name '{name}' does not match directory '{SKILL.name}'")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("Skill name violates the Agent Skills naming rule")
    if not 1 <= len(description) <= 1024:
        fail("Skill description must contain 1-1024 characters")
    if len(body.splitlines()) > 500:
        fail("SKILL.md body exceeds the recommended 500-line limit")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    frontmatter_text = skill_md.read_text(encoding="utf-8").split("---", 2)[1]
    version_match = re.search(r"^\s+version:\s*[\"']?([^\"'\s]+)", frontmatter_text, re.M)
    if not version_match or version_match.group(1) != version:
        fail("SKILL.md metadata version does not match VERSION")

    required_refs = {
        "references/writing-style.md",
        "references/platform-rules.md",
        "references/quality-review.md",
        "references/title-review.md",
        "references/fact-checking.md",
        "references/privacy-and-compliance.md",
        "references/cover-style.md",
        "references/examples.md",
    }
    for ref in required_refs:
        if not (SKILL / ref).is_file():
            fail(f"Required skill reference is missing: {ref}")


def validate_plugin() -> None:
    path = ROOT / "plugin.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Invalid plugin.json: {exc}")
        return
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        fail("plugin.json must target Agent Plugins 1.0.0")
    if manifest.get("name") != "hou-content-creator":
        fail("plugin.json name is incorrect")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        fail("plugin.json version does not match VERSION")
    allowed = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
    unknown = set(manifest) - allowed
    if unknown:
        fail(f"plugin.json contains unsupported root fields: {sorted(unknown)}")


def validate_openai_config() -> None:
    path = SKILL / "agents" / "openai.yaml"
    text = path.read_text(encoding="utf-8")
    for key in ("display_name:", "short_description:", "default_prompt:", "brand_color:", "allow_implicit_invocation:"):
        if key not in text:
            fail(f"openai.yaml is missing {key}")
    if "$hou-content-creator" not in text:
        fail("openai.yaml default_prompt must mention $hou-content-creator")
    if "products:" in text:
        fail("openai.yaml contains the unsupported policy.products field")
    for asset in ("./assets/icon.svg",):
        if asset not in text:
            fail(f"openai.yaml does not reference {asset}")


def validate_examples() -> None:
    example_dir = ROOT / "examples"
    expected = {
        "wechat-polish.md",
        "short-video-script.md",
        "zhihu-edit.md",
        "xiaohongshu-adaptation.md",
        "x-and-moments.md",
        "title-optimization.md",
        "quality-review.md",
    }
    present = {path.name for path in example_dir.glob("*.md") if path.name != "README.md"}
    if present != expected:
        fail(f"Example set differs from expected files: {sorted(expected ^ present)}")
    for name in expected:
        text = (example_dir / name).read_text(encoding="utf-8")
        for heading in ("## 原始素材", "## 用户指令", "## 示例输出", "## 审核结果"):
            if heading not in text:
                fail(f"examples/{name} is missing '{heading}'")


def validate_markdown_links() -> None:
    link_pattern = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", "dist"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / target).resolve()
            try:
                target_path.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"Link escapes repository in {path.relative_to(ROOT)}: {target}")
                continue
            if not target_path.exists():
                fail(f"Broken link in {path.relative_to(ROOT)}: {target}")


def validate_assets_and_secrets() -> None:
    for relative in ("docs/images/cover.png", "docs/images/workflow.svg", "skills/hou-content-creator/assets/icon.svg"):
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"Missing or empty asset: {relative}")
    secret_patterns = {
        "GitHub token": re.compile(r"gh[oprsu]_[A-Za-z0-9]{20,}"),
        "OpenAI key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "dist"} for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in secret_patterns.items():
            if pattern.search(text):
                fail(f"Possible {label} in {path.relative_to(ROOT)}")


def main() -> int:
    validate_skill()
    validate_plugin()
    validate_openai_config()
    validate_examples()
    validate_markdown_links()
    validate_assets_and_secrets()
    for message in WARNINGS:
        print(f"WARNING: {message}")
    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}")
        print(f"Validation failed with {len(ERRORS)} error(s).")
        return 1
    print("Validation passed: skill, plugin, links, examples, assets, and secret scan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
