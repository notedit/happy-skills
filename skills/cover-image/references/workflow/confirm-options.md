# Confirm Options Workflow

## Step 2: Confirm Options

After analyzing content, confirm the 6 dimensions and provider with the user.

### Skip Conditions

| Condition | What's Skipped | What's Still Asked |
|-----------|----------------|-------------------|
| `--quick` flag | All 6 dimensions + provider | Aspect ratio (unless `--aspect` specified) |
| All 6 dimensions + `--aspect` + `--provider` specified | Everything | Nothing |
| Some dimensions specified | Only specified ones | Unspecified dimensions + aspect ratio |

### Confirmation Flow

```
1. Display auto-selected options
2. Ask user to confirm or modify
3. If modified, validate choice
4. Proceed to prompt creation
```

### Confirmation Message Template

```
Cover Image Options:

Content: [title/topic]
Language: [detected language]

Dimensions:
- Type: [type] -- [brief reason]
- Palette: [palette] -- [brief reason]
- Rendering: [rendering] -- [brief reason]
- Text: [text level]
- Mood: [mood]
- Font: [font]

Provider: [provider] -- [brief reason]
Aspect: [ratio] (default: 16:9)
Output: [directory path]

Proceed? [y/n] or modify: [type=X palette=Y provider=Z ...]
```

### Quick Mode

When `--quick` is set, skip confirmation entirely:

1. Auto-select all dimensions
2. Auto-select provider based on language and references
3. Use default aspect ratio (16:9) unless `--aspect` specified
4. Proceed directly to prompt creation
5. Show selections in completion report

### Dimension Validation

When user provides a value, validate it exists:

| Dimension | Valid Values |
|-----------|--------------|
| Type | hero, conceptual, typography, metaphor, scene, minimal |
| Palette | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro |
| Rendering | flat-vector, hand-drawn, painterly, digital, pixel, chalk |
| Text | none, title-only, title-subtitle, text-rich |
| Mood | subtle, balanced, bold |
| Font | clean, handwritten, serif, display |
| Provider | qwen, openai, google |
| Aspect | 16:9, 2.35:1, 4:3, 3:2, 1:1, 3:4 |

If invalid, show valid options and ask again.

### Provider Selection

When provider is not specified, auto-select based on signals:

| Signals | Provider |
|---------|----------|
| Chinese title detected | `qwen` |
| Reference images provided | `google` (or `openai`) |
| No special signals | `qwen` (default) |

### Aspect Ratio Selection

When aspect ratio is not specified, ask separately:

```
Aspect Ratio Options:
- 16:9 (default) -- Widescreen, blog posts
- 2.35:1 -- 公众号封面 (900x383px)
- 4:3 -- Classic, presentations
- 3:2 -- Photography standard
- 1:1 -- Square, social media
- 3:4 -- Portrait, mobile

Select aspect ratio: [default: 16:9]
```

### Platform Mapping

| Ratio | Platform | Size |
|-------|----------|------|
| `2.35:1` | 微信公众号封面 | 900x383px |
| `16:9` | 通用宽屏 | 1920x1080px |
| `1:1` | 小红书/Instagram | 1080x1080px |
| `3:4` | 手机海报 | 1080x1440px |
