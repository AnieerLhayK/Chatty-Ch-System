# Chatty-Ch-System

[English](README.md)

Chatty Ch System 将语料预处理、角色技能生成、诊断和维护收拢为一个公开工程系统。
QQ 原始材料过滤器是系统内部模块。公开内容不包含私人语料、个人词库、已完成角色、
运行时记忆或私有报告。

## 模块

各模块位于 `packages/character-system/engineering/`：

- `corpus-preparation/qq-raw-material-filter`：解析 QCE v5 导出、评分分桶、审计词库并生成复核样本。
- `generation/character-generator`：从经过复核且获授权的材料生成风格启发型技能。
- `diagnosis/style-doctor`：诊断风格漂移与运行时输出问题。
- `maintenance/character-maintainer`：维护技能并审查补丁。

包内协议位于 `packages/character-system/shared/`，可移植的工作区策略位于 `shared/`。
[Frame for AI Workspace](https://github.com/AnieerLhayK/Frame-for-AI-workspace) 提供宿主框架；
在其他宿主使用时保留包布局及协议。

## 安装和运行 filter

在仓库根目录安装：

```bash
python -m pip install -e packages/character-system/engineering/corpus-preparation/qq-raw-material-filter
qce-block-filter --help
```

将 `AI_ROOT` 设置为自己的绝对数据根。PowerShell 示例为
`$env:AI_ROOT = 'C:/my-materials'`；POSIX shell 示例为 `export AI_ROOT=/my/materials`。
输入、输出、词库及复核决策默认位于该根下的
`raw_material/qq/exports/character.<writer_name>/`。

```bash
cd packages/character-system/engineering/corpus-preparation/qq-raw-material-filter
python qce_block_filter.py --writer-name sample --me-id 123456789
```

使用 `--input-dir`、`--output-dir` 覆盖输入与输出。
配置中的相对词库或复核路径仍需要 `AI_ROOT`。要求 Python 3.11+。
处理在本地完成，原始导出保持只读。

## 与生成器交接

人工复核分桶 JSONL，并对选中材料脱敏。将获准材料整理为 `.txt`、`.md` 或 `.docx`，
再配置生成器的语料来源；生成器不直接接收分桶 JSONL。
`need_anonymize` 是待脱敏材料，不能直接当作已批准语料。

在 `packages/character-system/engineering/generation/character-generator/` 运行生成器。
将示例配置复制到忽略的私人配置位置，填写经复核的语料来源；在运行时暴露前检查技能及报告。

## 验证

```bash
python -m pip install pytest
python scripts/check_public_package.py --dir .
```

检查器验证公开边界，并分别在模块目录运行测试。
CI 另在 Python 3.11、3.12 上安装 filter 并检查 CLI。
测试默认使用合成输入；可选真实样本必须显式设置 `QCE_SAMPLE_DATA_DIR`，不得提交。

## 维护与来源

本仓库是权威 workspace package 的生成式公开投影。
业务源码及可移植投影规则由 `character-system` 拥有；本机路径、远端注册、TASK 授权及
聚合同步由宿主拥有。不要恢复独立 filter publisher，或将生成 checkout 当作源码维护。
`PROJECTION_SOURCE.json` 标识对应源码版本。

旧 [qq-chat-raw-filter](https://github.com/AnieerLhayK/qq-chat-raw-filter) 仓库退役并保留历史，
其功能在本系统维护。

双语导航和 filter 的隐私说明参考未合并的
[filter 文档 PR #1](https://github.com/AnieerLhayK/qq-chat-raw-filter/pull/1) 及
[Chatty 文档 PR #1](https://github.com/AnieerLhayK/Chatty-Ch-System/pull/1)。
本地 package 是权威源，不自动合并这些 PR。
