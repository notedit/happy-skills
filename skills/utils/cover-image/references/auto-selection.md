# Auto-Selection Rules

When a dimension is omitted, select based on content signals.

## Auto Type Selection

| Signals (EN/CN) | Type |
|-----------------|------|
| Product, launch, announcement, release, reveal / 产品发布, 公告, 上线 | `hero` |
| Architecture, framework, system, API, technical, model / 架构, 框架, 系统, 技术 | `conceptual` |
| Quote, opinion, insight, thought, headline, statement / 观点, 金句, 见解 | `typography` |
| Philosophy, growth, abstract, meaning, reflection / 哲学, 成长, 思考 | `metaphor` |
| Story, journey, travel, lifestyle, experience, narrative / 故事, 旅程, 生活 | `scene` |
| Zen, focus, essential, core, simple, pure / 极简, 核心, 本质 | `minimal` |

## Auto Palette Selection

| Signals (EN/CN) | Palette |
|-----------------|---------|
| Personal story, emotion, lifestyle, human / 个人故事, 情感, 生活 | `warm` |
| Business, professional, thought leadership, luxury / 商业, 专业, 奢侈 | `elegant` |
| Architecture, system, API, technical, code / 架构, 系统, 代码 | `cool` |
| Entertainment, premium, cinematic, dark mode / 娱乐, 高端, 电影感 | `dark` |
| Nature, wellness, eco, organic, travel / 自然, 健康, 环保 | `earth` |
| Product launch, gaming, promotion, event / 产品发布, 游戏, 推广 | `vivid` |
| Fantasy, children, gentle, creative, whimsical / 童趣, 创意, 梦幻 | `pastel` |
| Zen, focus, essential, pure, simple / 禅意, 纯粹, 简洁 | `mono` |
| History, vintage, retro, classic, exploration / 历史, 复古, 经典 | `retro` |

## Auto Rendering Selection

| Signals (EN/CN) | Rendering |
|-----------------|-----------|
| Clean, modern, tech, WeChat, icon-based, infographic / 现代, 科技, 图标 | `flat-vector` |
| Sketch, note, personal, casual, doodle, warm / 手绘, 笔记, 随意 | `hand-drawn` |
| Art, watercolor, soft, dreamy, creative, fantasy / 艺术, 水彩, 梦幻 | `painterly` |
| Data, dashboard, SaaS, corporate, polished / 数据, 企业, 精致 | `digital` |
| Gaming, retro, 8-bit, nostalgic / 游戏, 复古, 像素 | `pixel` |
| Education, tutorial, classroom, teaching / 教育, 教程, 课堂 | `chalk` |

## Auto Text Selection

| Signals (EN/CN) | Text Level |
|-----------------|------------|
| Visual-only, photography, abstract, art / 纯视觉, 摄影, 抽象 | `none` |
| Article, blog, standard cover / 文章, 博客, 标准封面 | `title-only` |
| Series, tutorial, technical with context / 系列, 教程, 技术文 | `title-subtitle` |
| Announcement, features, multiple points, infographic / 公告, 特性, 信息图 | `text-rich` |

Default: `title-only`

## Auto Mood Selection

| Signals (EN/CN) | Mood Level |
|-----------------|------------|
| Professional, corporate, thought leadership, academic, luxury / 专业, 学术, 高端 | `subtle` |
| General, educational, standard, blog, documentation / 通用, 教育, 文档 | `balanced` |
| Launch, announcement, promotion, event, gaming, entertainment / 发布, 推广, 游戏 | `bold` |

Default: `balanced`

## Auto Font Selection

| Signals (EN/CN) | Font |
|-----------------|------|
| Personal, lifestyle, human, warm, friendly, story / 个人, 生活, 温暖 | `handwritten` |
| Technical, professional, clean, modern, minimal, data / 技术, 专业, 现代 | `clean` |
| Editorial, academic, luxury, classic, literary / 编辑, 学术, 经典 | `serif` |
| Announcement, entertainment, promotion, bold, event, gaming / 公告, 娱乐, 游戏 | `display` |

Default: `clean`

## Auto Provider Selection

| Signals | Provider |
|---------|----------|
| Chinese title detected | `qwen` |
| Reference images provided | `google` (or `openai`) |
| `--style tech-*` preset | `qwen` |
| Default | `qwen` |
