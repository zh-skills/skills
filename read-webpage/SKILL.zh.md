---
name: read-webpage
description: 读取任何公开网页的纯文字内容。仅当用户明确输入 "use skill read-webpage"、"用技能读网页"（简体中文）或 "用技能讀網頁"（繁体中文）并附上网址时才触发。请勿对通用的"读网页"或"获取页面"短语触发——这些应使用平台内置的网页读取工具。
---

# 读取网页技能（read-webpage）

> 本文件供人类用户阅读。AI 平台将读取英文版 [SKILL.md](SKILL.md) 来运行此技能。

> English version: [SKILL.md](SKILL.md)

读取任何公开网页的纯文字内容，去除所有 HTML 标签、脚本及导航杂讯，并将完整内容保存至 .txt 文件。

## 工作流程

1. 从消息中提取网址
2. 执行 `scripts/read_webpage.py {网址}` 读取并清理网页内容
3. 将完整文字保存至以网址及日期时间命名的 `.txt` 文件
4. 向用户显示预览内容及已保存的文件名称

## 触发示例

- `use skill read-webpage https://en.wikipedia.org/wiki/Artificial_intelligence`
- `use skill read-webpage https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans`（简体中文）
- `use skill read-webpage https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant`（繁体中文）
- `用技能读网页 https://zh.wikipedia.org/wiki/人工智能?variant=zh-hans`（简体中文触发）
- `用技能讀網頁 https://zh.wikipedia.org/wiki/人工智能?variant=zh-hant`（繁体中文触发）

若网页返回少于 5 行（例如 `https://quotes.toscrape.com/js/`），表示该网页为 JavaScript 动态加载，建议改用 `read-webpage-advanced` 技能。

## 输出格式

```
📄 网页预览：{网址}

{前 800 个字符的纯文字内容}

【已读取 {N} 行 • 已保存至 {文件名}_{YYYYMMDD_HHMMSS}.txt】
```

完整文字保存至以完整网址及日期时间命名的 `.txt` 文件（例如：`zh.wikipedia.org_wiki_人工智能_variant=zh-hans_20260330_143022.txt`）。

若网页无法读取，将显示 HTTP 错误信息。若读取行数少于 5 行，表示该网页使用 JavaScript 动态加载内容，建议改用 `read-webpage-advanced` 技能，且不保存文件。

## 语言检测

脚本会自动检测用户输入的语言并相应地调整输出：

- 若输入包含中文字符（`\u4e00-\u9fff`），则使用中文输出
- 若检测到繁体中文专用字符（如 `網`、`頁`、`讀`、`儲`），则使用繁体中文
- 若检测到中文但无繁体标志，则默认使用简体中文
- 若无中文字符，则使用英文

输出信息（预览标题、读取行数、文件名）将根据检测到的语言本地化显示。保存的 `.txt` 文件内容始终为网页原始语言。

## 重要提示

每次请求只执行一次脚本，每次执行只保存一个 `.txt` 文件。重试前请先确认是否已有保存的文件——若已有，表示执行成功，无需重试。

详细实现说明请参阅 [references/api_reference.md](references/api_reference.md)。

## 安装

```bash
git clone https://github.com/zh-skills/skills
```

或使用 skills CLI：

```bash
npx skills add zh-skills/skills@read-webpage
```

## 依赖包

```bash
pip install requests beautifulsoup4
```

## 限制

- 仅支持静态 HTML 网页（不支持 JavaScript 动态加载内容）
- 仅支持公开网址（不支持需要登录的网页）
- 预览内容默认上限为 800 个字符
- 若网页返回少于 5 行，建议改用 `read-webpage-advanced` 技能
