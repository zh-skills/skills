---
name: speak-cantonese-save
description: Speak a Cantonese sentence aloud and save the audio as an mp3 file in the current directory. Use ONLY when the user explicitly says "use skill speak-cantonese-save" followed by a Cantonese sentence. The mp3 file is saved in the current directory — do NOT create subdirectories.
---

# Speak Cantonese Save

> 中文版本：[SKILL.zh.md](SKILL.zh.md)

Speak a Cantonese sentence aloud using edge-tts and save the audio as an mp3 file in the current directory.

## Workflow

1. Extract the sentence from the user's message (everything after "use skill speak-cantonese-save")
2. Run `scripts/speak_cantonese_save.py {sentence}` — speaks and saves mp3 to current directory
3. Report the saved filename to the user

## Trigger Examples

- `use skill speak-cantonese-save 各個國家有各個國家嘅國歌`
- `use skill speak-cantonese-save 一蚊一隻雞，一蚊一隻龜`

## Output Format

```
🔊 Spoke and saved: {sentence}
[Saved to {filename}.mp3]
```

## Important

- Run `scripts/speak_cantonese_save.py` only once per request
- The mp3 is saved in the current directory — no subdirectory is created
- After the script exits with code 0, report the saved filepath to the user and STOP
- Do NOT open, play, move, or search for the mp3 file
- Do NOT retry
