---
name: join-mp3
description: Join all mp3 files in a subfolder into a single mp3 file saved in the current directory. Files are joined in alphabetical order. Use ONLY when the user explicitly says "use skill join-mp3" followed by a subfolder name.
---

# Join MP3

Join all mp3 files in a subfolder into one combined mp3 file, saved in the current directory.

## Workflow

1. Extract the subfolder name from the user's message
2. Run `scripts/join_mp3.py {subfolder}` — joins all mp3 files alphabetically
3. Report the output filename to the user

## Trigger Examples

- `use skill join-mp3 speeches`
- `use skill join-mp3 cantonese_audio`

## Output Format

```
✅ Joined {N} files from {subfolder}/
[Saved to {output_filename}.mp3]
```

## Limits

- Per file: max 10 MB (larger files are skipped with a warning)
- Total: max 50 MB across all files
- File count: max 50 files

## Important

- Run `scripts/join_mp3.py` only once per request
- Files are joined in alphabetical order (which matches date-time filenames)
- Do NOT retry if the script exits with code 0
- Do NOT open or play the output file
