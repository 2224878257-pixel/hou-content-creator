# 参与贡献

感谢你帮助改进 Hou Content Creator。项目优先接受能提高真实性、可复用性、跨平台兼容性和中文表达质量的修改。

## 开始之前

1. 搜索现有 Issue，避免重复。
2. 大范围调整工作流程前先开 Issue 说明问题、使用场景和预期行为。
3. 不要提交真实客户资料、聊天记录、个人信息、密钥或未经授权的文章。
4. 示例必须明确标注为虚构教学素材，或提供可公开使用的授权说明。

## 本地检查

需要 Python 3.10 或更高版本，无第三方依赖。

```bash
python scripts/validate_project.py
python scripts/package_release.py
```

如果本机安装了 GitHub CLI 2.90.0 或更高版本，再运行：

```bash
gh skill publish --dry-run
```

## 修改原则

- `SKILL.md` 保持简洁，详细规则放入 `references/`，并使用相对路径引用。
- 新规则要说明何时适用，避免所有内容强制使用同一结构。
- 不添加无法核实的平台能力、安装命令或效果宣称。
- 调整质量评分时同步更新中英文 README 和相关示例。
- 修改版本时同步更新 `VERSION`、`plugin.json`、技能元数据和 `CHANGELOG.md`。

## Pull Request

请说明解决的问题、主要改动、验证命令和可能影响的宿主。视觉变更请附截图；规则变更请附最小示例。提交即表示你有权以本项目 MIT License 提供相应内容。
