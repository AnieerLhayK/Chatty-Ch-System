# e-Chatter 受管发行版

ai-workbench 是唯一开发源。此目录通过手动晋升接收不可覆盖、可独立构建的版本化
源码快照；修复返回 ai-workbench，不直接编辑快照。

candidate.json 选择最新本地候选版；全部稳定验收通过后才建立 stable.json。
两者指向 versions/ 下的快照，并记录源码提交和共享 Windows ZIP 的 SHA-256。
开发端与 character-system 的发行记录引用同一产物，二进制保存在源码树外。

进入所选版本的 README 查看独立使用和构建说明。用户解压 ZIP 即可启动，无需
Python／Node，自行安装并登录受支持的 Agent。发行包不包含个人角色。

公开投影仅包含明确批准的 0.2.0-rc.2 候选快照。下载入口为 Chatty-Ch-System
的 `e-chatter-v0.2.0-rc.2` Pre-release；此构建尚未重新完成真实 Codex、DeepSeek
账户／Key 和干净 Windows 11 验收，不替代稳定版。此包包含修订后的 Generator、
Doctor、Maintainer 指令；应用界面和候选审查流程保持一致。
