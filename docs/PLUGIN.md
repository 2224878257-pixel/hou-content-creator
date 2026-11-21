# Agent Plugin 说明

仓库根目录的 `plugin.json` 使用 Agent Plugins 1.0.0 schema，技能位于 `skills/hou-content-creator/`。插件不依赖 MCP 服务、远程凭据、应用连接或生命周期 Hook。

## 本地验证

```bash
python scripts/validate_project.py
python scripts/package_release.py
```

`dist/hou-content-creator-plugin-v1.0.1.zip` 是完整插件包；`dist/hou-content-creator-v1.0.1.zip` 是只包含独立技能的安装包。

## 发布状态

配置仅用于本地导入、测试和后续分发准备。项目尚未提交 OpenAI、Cursor、Claude 或其他公共插件目录，也没有宣称通过审核。公开提交涉及发布者资料、支持与隐私页面、审核材料等外部流程，必须由维护者确认后执行。
