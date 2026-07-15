# Chatty Ch System

[English](README.md)

Chatty Ch System 是一个面向风格启发型聊天与写作机器人的角色技能系统公开工程层，用于构建、诊断和维护技能。它不包含任何已完成角色、私人语料、运行时记忆或个人材料。

建议在 [Frame for AI Workspace](https://github.com/AnieerLhayK/Frame-for-AI-workspace) 中使用本仓库；该工作区已提供任务路由、共享策略、验证与迁移规则。若复制到其他受治理工作区，请保留包结构和共享协议。

## 包含内容

- `character-generator`：根据获授权或公开语料创建角色技能。
- `style-doctor`：诊断风格漂移和运行时输出问题。
- `character-maintainer`：在补丁和版本变更中维护已生成技能。
- `packages/character-system/shared`：schema、模板、漂移分类、补丁协议、交接格式和运行时循环策略。
- `shared`：理解包迁移与治理所需的可移植工作区策略。

## 不包含内容

- 运行时角色目录、私人或个人语料。
- 私有工作区中的诊断、交接、验证或补丁报告。
- 已完成工具包发行包、本机绝对路径或机器专属配置。

## 快速检查

```bash
python scripts/check_public_package.py --dir .
cd packages/character-system/engineering/generation/character-generator
python -m pytest tests -q
```

## 基本使用

1. 将获授权或公开的源材料放入已忽略的本地 `corpus/` 目录。
2. 将 `configs/character_config.example.json` 复制到私有配置路径，填写角色 ID、显示名、语料来源、目标任务和隐私设置。
3. 在生成器目录运行生成器；暴露到运行时平台前，先检查生成的技能和报告。

生成的角色技能是风格启发型写作工具，不是身份模拟器、冒充机器人、私人事实推断工具或语料重建工具。
