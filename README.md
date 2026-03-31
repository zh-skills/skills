# zh-skills — AI Agent Skills

A collection of AI agent skills for Chinese and English users. Install with one command and use with natural language.

> 中文用户：每个技能文件夹内均有 `SKILL.zh.md` 中文说明文件。

---

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [read-webpage](read-webpage/) | Fetch plain text from any static webpage. Supports English, Simplified and Traditional Chinese output. | `npx skills add zh-skills/skills@read-webpage` |
| [read-dynamic-webpage](read-dynamic-webpage/) | Fetch plain text from JavaScript-rendered pages using a headless browser (Playwright). | `npx skills add zh-skills/skills@read-dynamic-webpage` |
| [speak-cantonese](speak-cantonese/) | Convert a Cantonese sentence or text file to speech. Supports online (edge-tts) and local (macOS/Windows) modes. Includes Cantonese tongue-twister practice files. | `npx skills add zh-skills/skills@speak-cantonese` |

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
use skill speak-cantonese 各個國家有各個國家嘅國歌
use skill speak-cantonese file skills/speak-cantonese/assets/cantonese-challenge-1.txt
```

---

## When to Use Which Skill

- **read-webpage** — fast, no setup, works on most pages (Wikipedia, news, university sites)
- **read-dynamic-webpage** — slower, requires Playwright, handles JavaScript-rendered pages
- **speak-cantonese** — text-to-speech for Cantonese, online (edge-tts) or local (macOS/Windows) mode

If `read-webpage` returns fewer than 5 lines, the page is JS-rendered — switch to `read-dynamic-webpage`.

---

## Dependencies

```bash
# read-webpage
pip install requests beautifulsoup4

# read-dynamic-webpage
pip install playwright beautifulsoup4
playwright install chromium

# speak-cantonese
pip install edge-tts pygame
```

---

## License

MIT
