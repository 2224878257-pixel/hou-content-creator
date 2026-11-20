# 侯同学·内容创作助手

**Hou Content Creator** · Agent Skill · v1.0.0

一套从选题、查证、写作到内容审核的中文自媒体创作技能。适合想用 AI 记录真实经历、研究商业机会、分享专业知识的创作者。

## 功能

- 公众号文章、知乎回答、小红书笔记、短视频口播、B站脚本、X 和朋友圈文案。
- 自然、口语化表达，保留真实判断与具体细节。
- 标题优化、封面文案、视觉风格和跨平台适配。
- 核对案例、数据和来源，区分事实、观点、假设与计划。
- 十项内容质量审核，先检查、再修改、最后交付。

## 使用方式

下载本仓库，将完整的 `hou-content-creator/` 目录导入支持 Agent Skills 的工具，保留其中的 `SKILL.md`、`references/`、`agents/` 和 `assets/`。具体安装入口取决于工具及其版本。

使用示例：

```text
使用 $hou-content-creator，把下面的素材写成一篇公众号文章。
使用 $hou-content-creator，检查这篇文章是否自然、有真实依据。
使用 $hou-content-creator，把我的文章改写成一分钟口播稿。
```

也可以在支持读取文件的工具中直接要求读取 `hou-content-creator/SKILL.md` 并按其引用的规则执行。

## 自定义

在 `references/writing-style.md` 中替换品牌定位、受众和表达偏好，在 `references/cover-style.md` 中调整视觉规范，在 `references/quality-review.md` 中调整审核标准。真实经历应由使用者明确提供，不要将示例当作自己的经历。

## 目录

```text
hou-content-creator/
├── SKILL.md
├── agents/openai.yaml
├── assets/icon.svg
└── references/
    ├── writing-style.md
    ├── platform-rules.md
    ├── quality-review.md
    ├── cover-style.md
    └── examples.md
```

本项目不包含 API 密钥，不依赖独立运行脚本，也不会自动发布内容。联网核实及图片生成能力取决于宿主工具。

## 许可

MIT License。欢迎使用、修改和分享。不代表对第三方数据、商标或平台内容授予额外许可。
