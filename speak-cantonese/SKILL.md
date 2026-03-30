---
name: speak-cantonese
description: Speak a Cantonese sentence aloud using text-to-speech. Use ONLY when the user explicitly says "use skill speak-cantonese" followed by a Cantonese sentence. The script speaks the audio directly — do NOT search for or expect any mp3 file to be saved.
---

# Speak Cantonese

> 中文版本：[SKILL.zh.md](SKILL.zh.md)

Speak a Cantonese sentence aloud using edge-tts (online) or macOS system voice (local).

## Workflow

1. Extract the sentence from the user's message (everything after "use skill speak-cantonese")
2. Run `scripts/speak_cantonese.py {sentence}` — the script speaks the audio and exits
3. Report the result to the user
4. Do NOT search for mp3 files. Do NOT retry. The task is complete when the script exits.

## Trigger Examples

- `use skill speak-cantonese 各個國家有各個國家嘅國歌` — default (online, edge-tts)
- `use skill speak-cantonese online 各個國家有各個國家嘅國歌` — explicitly use edge-tts
- `use skill speak-cantonese local 各個國家有各個國家嘅國歌` — use macOS system voice (Sinji)

## Modes

- `online` (default) — uses edge-tts (Microsoft zh-HK-HiuMaanNeural, free, requires internet)
- `local` — uses macOS `say` command with Sinji (Cantonese HK) voice
- If the chosen mode fails, automatically falls back to the other mode

## Output Format

```
🔊 Spoke (online): {sentence}
```
or
```
🔊 Spoke (local, Sinji): {sentence}
```

## Important

- Run `scripts/speak_cantonese.py` only once per request
- The script plays audio directly and exits — no mp3 file is saved
- Do NOT search for mp3 files after running
- Do NOT retry if the script exits with code 0

## Setup

```bash
pip install edge-tts    # for online mode (default, auto-installed if missing)
```

macOS local mode uses the built-in `say` command — no install needed. Install Sinji (Cantonese HK) voice in System Settings → Accessibility → Spoken Content.

## Reference

For implementation details see [references/implementation_notes.md](references/implementation_notes.md).
