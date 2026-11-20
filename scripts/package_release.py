#!/usr/bin/env python3
"""Build deterministic standalone-skill and portable-plugin release archives."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILL = ROOT / "skills" / "hou-content-creator"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def add_file(archive: zipfile.ZipFile, source: Path, destination: str) -> None:
    info = zipfile.ZipInfo(destination.replace("\\", "/"), ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def build_skill() -> Path:
    output = DIST / f"hou-content-creator-v{VERSION}.zip"
    with zipfile.ZipFile(output, "w") as archive:
        for source in sorted(path for path in SKILL.rglob("*") if path.is_file()):
            destination = Path("hou-content-creator") / source.relative_to(SKILL)
            add_file(archive, source, destination.as_posix())
        add_file(archive, ROOT / "LICENSE", "hou-content-creator/LICENSE")
    return output


def build_plugin() -> Path:
    output = DIST / f"hou-content-creator-plugin-v{VERSION}.zip"
    include_roots = [ROOT / "plugin.json", ROOT / "LICENSE", ROOT / "README.md", ROOT / "README_EN.md"]
    with zipfile.ZipFile(output, "w") as archive:
        for source in include_roots:
            add_file(archive, source, f"hou-content-creator/{source.name}")
        for source in sorted(path for path in SKILL.rglob("*") if path.is_file()):
            destination = Path("hou-content-creator/skills/hou-content-creator") / source.relative_to(SKILL)
            add_file(archive, source, destination.as_posix())
    return output


def main() -> None:
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        raise SystemExit("plugin.json version does not match VERSION")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    outputs = [build_skill(), build_plugin()]
    lines = []
    for output in outputs:
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        lines.append(f"{digest}  {output.name}")
        print(f"Built {output.relative_to(ROOT)}")
    (DIST / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Built dist/SHA256SUMS.txt")


if __name__ == "__main__":
    main()
