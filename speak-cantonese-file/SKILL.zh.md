---
name: speak-cantonese-file
description: 逐行读取文本文件并用粤语朗读，将每行保存为当前目录下的 mp3 文件。仅当用户明确输入 "use skill speak-cantonese-file" 后跟文件名时才触发。
---

# 粤语文件朗读技能（speak-cantonese-file）

> 本文件供人类用户阅读。AI 平台将读取英文版 [SKILL.md](SKILL.md) 来运行此技能。

> English version: [SKILL.md](SKILL.md)

逐行读取文本文件，使用 edge-tts 朗读每行粤语内容，并将每行保存为当前目录下的 mp3 文件。

## 工作流程

1. 从用户消息中提取文件名（"use skill speak-cantonese-file" 之后的所有内容）
2. 执行 `scripts/speak_cantonese_file.py {文件名}` — 逐行朗读并保存 mp3
3. 向用户显示结果

## 触发示例

- `use skill speak-cantonese-file cantonese-challenge-1.txt`
- `use skill speak-cantonese-file speech-Cantonese.txt`

## 输出格式

```
[1/N] {行内容}
[2/N] {行内容}
...
🔊 Spoke N lines from: {文件名}
[Saved N mp3 files in current directory]
```

## 重要提示

- 每次请求只执行一次脚本
- mp3 文件保存在当前目录——不创建子目录
- 若脚本以代码 0 退出，表示执行成功，无需重试
- 若文件不存在，脚本报错后退出

## 安装

```bash
pip install edge-tts    # 缺失时自动安装
```
