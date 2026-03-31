# zh-skills — AI Agent Skills

A collection of AI agent skills for Chinese and English users. Install with one command and use with natural language.

> 中文用户：每个技能文件夹内均有 `SKILL.zh.md` 中文说明文件。

---

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [read-webpage](read-webpage/) | Fetch plain text from any static webpage. Supports English, 简体中文, 繁體中文 output. | `npx skills add zh-skills/skills@read-webpage` |
| [read-dynamic-webpage](read-dynamic-webpage/) | Fetch plain text from JavaScript-rendered pages using Playwright headless browser. | `npx skills add zh-skills/skills@read-dynamic-webpage` |
| [speak-cantonese](speak-cantonese/) | Speak a Cantonese sentence aloud using edge-tts. | `npx skills add zh-skills/skills@speak-cantonese` |
| [speak-cantonese-save](speak-cantonese-save/) | Convert a Cantonese sentence to speech and save as mp3 in current directory. | `npx skills add zh-skills/skills@speak-cantonese-save` |
| [speak-cantonese-file](speak-cantonese-file/) | Read a text file line by line, save all lines as mp3, join into one file, then play. | `npx skills add zh-skills/skills@speak-cantonese-file` |
| [text-to-speech-cantonese](text-to-speech-cantonese/) | Convert a Cantonese sentence to speech and play it (combines speak-cantonese-save + play-mp3). | `npx skills add zh-skills/skills@text-to-speech-cantonese` |
| [play-mp3](play-mp3/) | Play an mp3 file using the system audio player. | `npx skills add zh-skills/skills@play-mp3` |
| [join-mp3](join-mp3/) | Join all mp3 files in a subfolder into one combined mp3 file. | `npx skills add zh-skills/skills@join-mp3` |

---

## Quick Start

### Install a skill
```bash
npx skills add zh-skills/skills@read-webpage
```

### Or clone the full collection
```bash
git clone https://github.com/zh-skills/skills
```

### Use a skill (in your AI chat)
```
use skill read-webpage https://en.wikipedia.org/wiki/Artificial_intelligence
用技能读网页 https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans
用技能讀網頁 https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant
use skill read-dynamic-webpage https://quotes.toscrape.com/js/
用技能讀動態網頁 https://quotes.toscrape.com/js/
use skill speak-cantonese 各個國家有各個國家嘅國歌
use skill text-to-speech-cantonese 各個國家有各個國家嘅國歌
use skill speak-cantonese-file cantonese-challenge-1.txt
use skill play-mp3 voice.mp3
use skill join-mp3 speeches
```

---

## When to Use Which Skill

- **read-webpage** — fast, no setup, works on most pages (Wikipedia, news, university sites)
- **read-dynamic-webpage** — slower, requires Playwright, handles JavaScript-rendered pages
- **speak-cantonese** — speak a sentence, no file saved
- **speak-cantonese-save** — speak and save mp3, then use play-mp3 to listen
- **text-to-speech-cantonese** — speak and play in one step (combines save + play)
- **speak-cantonese-file** — speak a whole text file, saves and plays as one combined mp3
- **play-mp3** — play any saved mp3 file
- **join-mp3** — combine multiple mp3 files into one

---

## Dependencies

```bash
# read-webpage
pip install requests beautifulsoup4

# read-dynamic-webpage
pip install playwright beautifulsoup4
python -m playwright install chromium

# speak-cantonese, speak-cantonese-save, text-to-speech-cantonese, speak-cantonese-file
pip install edge-tts

# join-mp3
# macOS:
brew install ffmpeg
# Windows:
winget install ffmpeg
# or download from https://ffmpeg.org/download.html and add to PATH
```

---

## License

MIT
