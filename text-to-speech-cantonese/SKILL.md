---
name: text-to-speech-cantonese
description: Convert a Cantonese sentence to speech and play it. Use ONLY when the user explicitly says "use skill text-to-speech-cantonese" followed by a Cantonese sentence. This skill runs two steps in sequence: first save the mp3 using speak-cantonese-save, then play it using play-mp3.
---

# Text to Speech Cantonese

Convert a Cantonese sentence to speech and play it by running two skills in sequence.

## Workflow

This skill has no script. Follow these two steps in order:

**Step 1 — Save the audio:**
Run `scripts/speak_cantonese_save.py {sentence}` from the `speak-cantonese-save` skill.
Wait for it to complete and note the saved filename from the output.

**Step 2 — Play the audio:**
Run `scripts/play_mp3.py {filename}` from the `play-mp3` skill, using the filename from Step 1.
Wait for it to complete.

## Trigger Examples

- `use skill text-to-speech-cantonese 各個國家有各個國家嘅國歌`
- `use skill text-to-speech-cantonese 一蚊一隻雞，一蚊一隻龜`

## Output Format

```
✅ Saved: {filepath}
🔊 Playing: {filename}
✅ Done
```

## Important

- Run each step only once
- Do NOT retry if both scripts exit with code 0
- Do NOT search for or move any files
