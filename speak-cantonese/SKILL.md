---
name: speak-cantonese
description: Speak a Cantonese sentence aloud using text-to-speech and save the audio to an mp3 file. Use ONLY when the user explicitly says "use skill speak-cantonese" followed by a Cantonese sentence. Saves the audio to speeches/ folder with a filename based on the date and time.
---

# Speak Cantonese

> 中文版本：[SKILL.zh.md](SKILL.zh.md)

Convert a Cantonese sentence to speech using edge-tts and save the audio as an mp3 file.

## Workflow

1. Extract the sentence from the user's message (everything after "use skill speak-cantonese")
2. Run `scripts/speak_cantonese.py {sentence}` to synthesise and play the audio
3. The script saves the audio to `speeches/` folder named by date and time
4. Present the saved filename to the user

## Trigger Examples

- `use skill speak-cantonese 各個國家有各個國家嘅國歌` — default (online, edge-tts)
- `use skill speak-cantonese online 各個國家有各個國家嘅國歌` — explicitly use edge-tts
- `use skill speak-cantonese local 各個國家有各個國家嘅國歌` — use system voice (macOS/Windows)
- `use skill speak-cantonese file skills/speak-cantonese/assets/cantonese-challenge-1.txt` — speak a file line by line

## Modes

- `online` (default) — uses edge-tts (Microsoft zh-HK-HiuMaanNeural, free, requires internet)
- `local` — uses macOS `say` command (Sin-ji voice) or Windows pyttsx3
- If the chosen mode fails, automatically falls back to the other mode
- Always reports which method was used

## Output Format

```
🔊 Speaking: {sentence}
   Using: {method}

[Saved to speeches/cantonese_{YYYYMMDD_HHMMSS}.mp3]
```

## Important

Run `scripts/speak_cantonese.py` only once per request. Each run saves exactly one `.mp3` file. The script does NOT play audio — it saves the file only. Do NOT retry if no audio is heard. Check for the saved `.mp3` file in `speeches/` to confirm success.

## Setup

```bash
pip install edge-tts pygame    # for online mode (default)
pip install pyttsx3            # for local mode on Windows
```

macOS local mode uses the built-in `say` command — no install needed. Install the Sin-ji (Cantonese HK) voice in System Settings → Accessibility → Spoken Content.

## Reference

For implementation details see [references/implementation_notes.md](references/implementation_notes.md).
