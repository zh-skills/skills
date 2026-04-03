# zh-skills — AI Agent Skills

A collection of AI agent skills for Chinese and English users. Install with one command and use with natural language.

> 中文用户：每个技能文件夹内均有 `SKILL.zh.md` 中文说明文件。

---

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [read-webpage](read-webpage/) | Fetch plain text from any static webpage. Supports English, 简体中文, 繁體中文 output. | `npx skills add zh-skills/skills@read-webpage` |
| [read-dynamic-webpage](read-dynamic-webpage/) | Fetch plain text from JavaScript-rendered pages using Playwright headless browser. | `npx skills add zh-skills/skills@read-dynamic-webpage` |

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
```

---

## When to Use Which Skill

- **read-webpage** — fast, no setup, works on most pages (Wikipedia, news, university sites)
- **read-dynamic-webpage** — slower, requires Playwright, handles JavaScript-rendered pages

If `read-webpage` returns very few lines, the page is JS-rendered — switch to `read-dynamic-webpage`.

---

## Dependencies

```bash
# read-webpage
pip install requests beautifulsoup4

# read-dynamic-webpage
pip install playwright beautifulsoup4
python -m playwright install chromium
```

---

## License

MIT
