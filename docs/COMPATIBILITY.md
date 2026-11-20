# 兼容性与安装核实记录

最后核实：2026-11-20。

## Agent Skills

技能目录符合 Agent Skills 规范：目录名与 `name` 一致，`SKILL.md` 包含必要 frontmatter，引用使用技能根目录的相对路径，详细规则按需加载。

来源：[Agent Skills specification](https://agentskills.io/specification)。

## GitHub CLI

GitHub CLI 2.90.0 起提供预览版 `gh skill`，能为 Codex、Claude Code、Cursor 等宿主选择正确目录和范围。本项目已使用 GitHub CLI 2.101.0 对 `gh skill publish --dry-run` 和安装发现流程进行验证。

来源：[GitHub CLI manual](https://cli.github.com/manual/gh_skill_install)。

## OpenAI Codex 与 ChatGPT

OpenAI 将 Skills 定义为可复用的说明与资源目录；插件可以打包 Skills、MCP 或两者。本仓库采用根 `plugin.json` 和 `skills/` 的可移植 Agent Plugins 结构。ChatGPT Skills 的账号与工作区可用性有限，官方说明没有确认从任意 GitHub 仓库一条命令安装，因此 README 只提供 Skills 编辑器导入路径。

来源：[Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)、[Package your plugin](https://developers.openai.com/plugins/build/plugins)。

## Claude Code

本项目通过 GitHub CLI 的 `--agent claude-code` 安装到 Claude Code 对应技能目录。Anthropic 官方示例也使用自包含的 `SKILL.md` 技能目录；其插件市场命令仅适用于已经配置为 Claude 插件市场的仓库，本项目不冒充已上架市场。

来源：[Anthropic Skills repository](https://github.com/anthropics/skills)。

## Cursor

Cursor 自动发现 `.agents/skills/`、`.cursor/skills/` 及用户级对应目录，也兼容 Claude 和 Codex 技能目录。Cursor 同时声明支持 Agent Plugins 开放标准。

来源：[Cursor Agent Skills](https://cursor.com/docs/skills)、[Cursor Plugins](https://cursor.com/docs/plugins)。

## 限制

兼容性表示结构和安装路径已核实，不代表所有宿主都提供联网搜索、图像生成或相同的显式调用语法。版本更新后应重新查阅官方文档。
