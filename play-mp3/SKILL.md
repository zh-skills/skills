---
name: play-mp3
description: Play an mp3 file. Use ONLY when the user explicitly says "use skill play-mp3" followed by a filename. The script plays the audio and exits — do NOT retry or search for files afterwards.
---

# Play MP3

Play an mp3 file using the system audio player.

## Workflow

1. Extract the filename from the user's message (everything after "use skill play-mp3")
2. Run `scripts/play_mp3.py {filename}` — plays the audio and exits
3. Report the result to the user

## Trigger Examples

- `use skill play-mp3 voice.mp3`
- `use skill play-mp3 cantonese_20260331_065110.mp3`

## Output Format

```
🔊 Playing: {filename}
✅ Done
```

## Important

- Run `scripts/play_mp3.py` only once per request
- Do NOT retry if the script exits with code 0
- If the file is not found, the script reports an error and exits
