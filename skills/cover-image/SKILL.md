---
name: cover-image
description: "Generate article cover images with 5 dimensions (type, palette, rendering, text, mood). Supports cinematic (2.35:1), widescreen (16:9), and square (1:1) aspects. Use when user asks to 'generate cover image', 'create article cover', or 'make cover'."
---

# Cover Image Generator

Generate elegant cover images for articles with 5-dimensional customization. Supports Chinese text rendering.

## Usage

```bash
# Auto-select dimensions based on content
/cover-image path/to/article.md

# Quick mode: skip confirmation
/cover-image article.md --quick

# Specify dimensions
/cover-image article.md --type conceptual --palette warm --rendering flat-vector

# WeChat Official Account cover
/cover-image article.md --aspect 2.35:1

# Specify provider
/cover-image article.md --provider qwen

# Use style preset
/cover-image article.md --style tech-dark

# Large font for better visibility
/cover-image article.md --font-size large

# Generate multiple options
/cover-image article.md --n 3

# With reference images (Google/OpenAI only)
/cover-image article.md --ref style-ref.png

# Direct content input
/cover-image --palette mono --aspect 1:1 --quick
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--type <name>` | hero, conceptual, typography, metaphor, scene, minimal |
| `--palette <name>` | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro |
| `--rendering <name>` | flat-vector, hand-drawn, painterly, digital, pixel, chalk |
| `--text <level>` | none, title-only, title-subtitle, text-rich |
| `--mood <level>` | subtle, balanced, bold |
| `--font <name>` | clean, handwritten, serif, display |
| `--font-size <size>` | small, medium (default), large, xlarge |
| `--aspect <ratio>` | 16:9 (default), 2.35:1 (公众号封面), 4:3, 3:2, 1:1, 3:4 |
| `--provider <name>` | qwen (default), openai, google |
| `--style <preset>` | tech-dark, tech-clean, lifestyle-warm, business-elegant, announcement-bold, minimal-zen, creative-playful, retro-vintage |
| `--lang <code>` | Title language (en, zh, ja, etc.) |
| `--no-title` | Alias for `--text none` |
| `--n <count>` | Number of images to generate (1-4) |
| `--quick` | Skip confirmation, use auto-selection |
| `--ref <files...>` | Reference images for style/composition guidance |

## Providers

| Provider | Model | Text Rendering | Chinese Support | Price |
|----------|-------|----------------|-----------------|-------|
| `qwen` | qwen-image-plus | Excellent | Native Chinese | 0.2 CNY/image |
| `openai` | gpt-image-1 | Good | Limited | ~$0.04/image |
| `google` | gemini-2.0-flash-exp | Good | Limited | Free tier available |

### Provider Selection Logic

1. `--provider` specified -> use it
2. Chinese title detected -> auto-select `qwen`
3. Reference images provided -> use `google` or `openai`
4. Default -> `qwen`

### Qwen-Image (Default)

Best for Chinese text rendering. Native support for Chinese characters.

**API Endpoint**: `https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

**Environment Variable**: `DASHSCOPE_API_KEY`

**Supported Sizes**: `1664*928`, `1024*1024`, `928*1664`, `1472*1104`, `1104*1472`

### OpenAI

Good for English text and creative designs.

**Environment Variable**: `OPENAI_API_KEY`

**Supported Sizes**: `1024x1024`, `1536x1024`, `1024x1536`

### Google

Good for multimodal generation with reference images.

**Environment Variable**: `GOOGLE_API_KEY`

**Supported Sizes**: Various aspect ratios supported

## Five Dimensions

| Dimension | Values | Default |
|-----------|--------|---------|
| **Type** | hero, conceptual, typography, metaphor, scene, minimal | auto |
| **Palette** | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro | auto |
| **Rendering** | flat-vector, hand-drawn, painterly, digital, pixel, chalk | auto |
| **Text** | none, title-only, title-subtitle, text-rich | title-only |
| **Mood** | subtle, balanced, bold | balanced |
| **Font** | clean, handwritten, serif, display | clean |

Auto-selection rules: [references/auto-selection.md](references/auto-selection.md)

## Galleries

**Types**: hero, conceptual, typography, metaphor, scene, minimal
-> Details: [references/types.md](references/types.md)

**Palettes**: warm, elegant, cool, dark, earth, vivid, pastel, mono, retro
-> Details: [references/palettes/](references/palettes/)

**Renderings**: flat-vector, hand-drawn, painterly, digital, pixel, chalk
-> Details: [references/renderings/](references/renderings/)

**Text Levels**: none (pure visual) | title-only (default) | title-subtitle | text-rich (with tags)
-> Details: [references/dimensions/text.md](references/dimensions/text.md)

**Mood Levels**: subtle (low contrast) | balanced (default) | bold (high contrast)
-> Details: [references/dimensions/mood.md](references/dimensions/mood.md)

**Fonts**: clean (sans-serif) | handwritten | serif | display (bold decorative)
-> Details: [references/dimensions/font.md](references/dimensions/font.md)

## File Structure

Output directory per `default_output_dir` preference:
- `same-dir`: `{article-dir}/`
- `imgs-subdir`: `{article-dir}/imgs/`
- `independent` (default): `cover-image/{topic-slug}/`

```
<output-dir>/
├── source-{slug}.{ext}    # Source files
├── refs/                  # Reference images (if provided)
│   ├── ref-01-{slug}.{ext}
│   └── ref-01-{slug}.md   # Description file
├── prompts/cover.md       # Generation prompt
└── cover.png              # Output image
```

**Slug**: 2-4 words, kebab-case. Conflict: append `-YYYYMMDD-HHMMSS`

## Workflow

### Progress Checklist

```
Cover Image Progress:
- [ ] Step 1: Analyze content + save refs + determine output dir
- [ ] Step 2: Confirm options (6 dimensions + provider) unless --quick
- [ ] Step 3: Create prompt
- [ ] Step 4: Generate image
- [ ] Step 5: Resize for platform (if needed)
- [ ] Step 6: Completion report
```

### Step 1: Analyze Content

1. **Save reference images** (if provided) -> [references/workflow/reference-images.md](references/workflow/reference-images.md)
2. **Save source content** (if pasted, save to `source.md`)
3. **Analyze content**: topic, tone, keywords, visual metaphors
4. **Deep analyze references**: Extract specific, concrete elements
5. **Detect language**: Compare source, user input
6. **Determine output directory**: Per File Structure rules
7. **Auto-select provider**: Based on language and references

### Step 2: Confirm Options

Full confirmation flow: [references/workflow/confirm-options.md](references/workflow/confirm-options.md)

| Condition | Skipped | Still Asked |
|-----------|---------|-------------|
| `--quick` | 6 dimensions + provider | Aspect ratio (unless `--aspect`) |
| All 6 + `--aspect` + `--provider` specified | All | None |

### Step 3: Create Prompt

Save to `prompts/cover.md`. Template: [references/workflow/prompt-template.md](references/workflow/prompt-template.md)

**CRITICAL - References in Frontmatter**:
- Files saved to `refs/` -> Add to frontmatter `references` list
- Style extracted verbally (no file) -> Omit `references`, describe in body
- Before writing -> Verify: `test -f refs/ref-NN-{slug}.{ext}`

**Reference elements in body** MUST be detailed, prefixed with "MUST"/"REQUIRED", with integration approach.

### Step 4: Generate Image

1. **Backup existing** `cover.png` if regenerating
2. **Select provider** based on language and options
3. **Process references** from prompt frontmatter:
   - `direct` usage -> pass reference images directly (google/openai only)
   - `style`/`palette` -> extract traits, append to prompt
4. **Generate** via provider API:
   - **Qwen**: POST to dashscope API, poll for result
   - **OpenAI**: Use ImageGen tool or API
   - **Google**: Use ImageGen tool with reference images
5. On failure: auto-retry once

### Step 5: Resize for Platform

Resize generated image to target platform size:

| Platform | Target Size | Aspect Ratio |
|----------|-------------|--------------|
| 公众号封面 | 900x383 | 2.35:1 |
| 博客/视频 | 1920x1080 | 16:9 |
| 小红书 | 1080x1080 | 1:1 |
| 手机海报 | 1080x1440 | 3:4 |

### Step 6: Completion Report

```
Cover Generated!

Provider: [provider]
Topic: [topic]
Type: [type] | Palette: [palette] | Rendering: [rendering]
Text: [text] | Mood: [mood] | Font: [font] | Aspect: [ratio]
Title: [title or "visual only"]
Language: [lang]
References: [N images or "extracted style" or "none"]
Location: [directory path]

Files:
- source-{slug}.{ext}
- prompts/cover.md
- cover.png
- cover-{platform}.png (if resized)
```

## Composition Principles

- **Whitespace**: 40-60% breathing room
- **Visual anchor**: Main element centered or offset left
- **Characters**: Simplified silhouettes; NO realistic humans
- **Title**: Use exact title from user/source; never invent

## Aspect Ratios

| Ratio | Platform | Use Case |
|-------|----------|----------|
| `2.35:1` | 微信公众号封面 | 公众号首图，900x383px |
| `16:9` | 通用宽屏 | 博客、视频封面 |
| `1:1` | 社交媒体 | 微博、小红书、Instagram |
| `4:3` | 经典比例 | 演示文稿、传统媒体 |
| `3:2` | 摄影标准 | 照片风格封面 |
| `3:4` | 竖版 | 手机端、海报 |

## Environment Variables

| Variable | Required For | Get From |
|----------|--------------|----------|
| `DASHSCOPE_API_KEY` | Qwen (default) | https://bailian.console.aliyun.com |
| `OPENAI_API_KEY` | OpenAI | https://platform.openai.com |
| `GOOGLE_API_KEY` | Google | https://aistudio.google.com |

## References

**Dimensions**: [text.md](references/dimensions/text.md) | [mood.md](references/dimensions/mood.md) | [font.md](references/dimensions/font.md)
**Palettes**: [references/palettes/](references/palettes/)
**Renderings**: [references/renderings/](references/renderings/)
**Types**: [references/types.md](references/types.md)
**Style Presets**: [references/style-presets.md](references/style-presets.md)
**Auto-Selection**: [references/auto-selection.md](references/auto-selection.md)
**Visual Elements**: [references/visual-elements.md](references/visual-elements.md)
**Workflow**: [confirm-options.md](references/workflow/confirm-options.md) | [prompt-template.md](references/workflow/prompt-template.md) | [reference-images.md](references/workflow/reference-images.md) | [qwen-api.md](references/workflow/qwen-api.md)
