---
name: speak-cantonese-file
description: Read a text file line by line and speak each line in Cantonese, saving each line as an mp3 file in the current directory. Use ONLY when the user explicitly says "use skill speak-cantonese-file" followed by a filename.
---

# Speak Cantonese File

> 中文版本：[SKILL.zh.md](SKILL.zh.md)

Read a text file line by line, speak each line in Cantonese using edge-tts, and save each line as an mp3 file in the current directory.

## Workflow

1. Extract the filename from the user's message (everything after "use skill speak-cantonese-file")
2. Run `scripts/speak_cantonese_file.py {filename}` — reads, speaks, and saves each line
3. Report the results to the user

## Trigger Examples

- `use skill speak-cantonese-file cantonese-challenge-1.txt`
- `use skill speak-cantonese-file speech-Cantonese.txt`

## Output Format

```
[1/N] {line}
[2/N] {line}
...
🔊 Spoke N lines from: {filename}
[Saved N mp3 files in current directory]
```

## Important

- Run `scripts/speak_cantonese_file.py` only once per request
- Mp3 files are saved in the current directory — no subdirectory is created
- Do NOT retry if the script exits with code 0
- If the file is not found, the script reports an error and exits
