---
name: speak-cantonese
description: 将粤语句子转换为语音并保存为 mp3 文件。仅当用户明确输入 "use skill speak-cantonese" 后跟粤语句子时才触发。音频保存至 speeches/ 文件夹，文件名包含日期和时间。
---

# 粤语朗读技能（speak-cantonese）

> 本文件供人类用户阅读。AI 平台将读取英文版 [SKILL.md](SKILL.md) 来运行此技能。

> English version: [SKILL.md](SKILL.md)

将粤语句子转换为语音，使用 edge-tts 合成并保存为 mp3 文件。

## 工作流程

1. 从用户消息中提取句子（"use skill speak-cantonese" 之后的所有内容）
2. 执行 `scripts/speak_cantonese.py {句子}` 合成并播放音频
3. 脚本将音频保存至 `speeches/` 文件夹，文件名包含日期和时间
4. 向用户显示已保存的文件名

## 触发示例

- `use skill speak-cantonese 各個國家有各個國家嘅國歌` — 默认（在线，edge-tts）
- `use skill speak-cantonese online 各個國家有各個國家嘅國歌` — 明确使用 edge-tts
- `use skill speak-cantonese local 各個國家有各個國家嘅國歌` — 使用系统语音（macOS/Windows）

## 模式说明

- `online`（默认）— 使用 edge-tts（微软 zh-HK-HiuMaanNeural，免费，需要网络）
- `local` — 使用 macOS `say` 命令（善怡 Sinji 语音）或 Windows pyttsx3
- 若所选模式失败，自动切换至另一模式
- 无论使用哪种模式，均会告知用户

## 输出格式

```
🔊 Speaking: {句子}
   Using: {使用的方法}

[Saved to speeches/cantonese_{YYYYMMDD_HHMMSS}.mp3]
```

## 重要提示

每次请求只执行一次脚本，每次执行只保存一个 `.mp3` 文件。重试前请先确认是否已有保存的文件——若已有，表示执行成功，无需重试。

## 安装

```bash
pip install edge-tts pygame    # 在线模式（默认）
pip install pyttsx3            # Windows 本地模式
```

macOS 本地模式使用内置 `say` 命令，无需安装。请在「系统设置 → 辅助功能 → 朗读内容」中安装善怡（Sinji，粤语香港）语音。

## 参考文档

详细实现说明请参阅 [references/implementation_notes.md](references/implementation_notes.md)。
