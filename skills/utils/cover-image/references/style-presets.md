# Style Presets

Quick style presets for common use cases. Use `--style <preset>` to apply.

## Available Presets

| Preset | Type | Palette | Rendering | Mood | Best For |
|--------|------|---------|-----------|------|----------|
| `tech-dark` | conceptual | dark | digital | bold | 科技文章、技术博客 |
| `tech-clean` | conceptual | cool | flat-vector | balanced | API文档、系统架构 |
| `lifestyle-warm` | scene | warm | painterly | subtle | 生活方式、个人故事 |
| `business-elegant` | hero | elegant | digital | subtle | 商业文章、专业报告 |
| `announcement-bold` | hero | vivid | flat-vector | bold | 产品发布、活动公告 |
| `minimal-zen` | minimal | mono | flat-vector | subtle | 极简设计、哲学思考 |
| `creative-playful` | metaphor | pastel | hand-drawn | balanced | 创意内容、儿童话题 |
| `retro-vintage` | scene | retro | painterly | subtle | 怀旧话题、历史内容 |

## Preset Details

### tech-dark

科技感黑色系，适合技术博客和科技文章。

```yaml
type: conceptual
palette: dark
rendering: digital
mood: bold
font: clean
```

**Prompt hints**:
- Deep black background (#000000)
- Electric blue accents (#3B82F6)
- Circuit patterns, geometric shapes
- Large bold title with glow effect

### tech-clean

清爽科技风，适合技术文档和架构图。

```yaml
type: conceptual
palette: cool
rendering: flat-vector
mood: balanced
font: clean
```

**Prompt hints**:
- Light gray background (#F7FAFC)
- Deep blue primary (#2B6CB0)
- Clean geometric icons
- Minimal decoration

### lifestyle-warm

温馨生活风，适合生活方式和个人故事。

```yaml
type: scene
palette: warm
rendering: painterly
mood: subtle
font: handwritten
```

**Prompt hints**:
- Warm cream background (#FFFAF0)
- Soft orange accents (#ED8936)
- Organic shapes, gentle gradients
- Friendly, approachable feel

### business-elegant

商务优雅风，适合商业文章和专业报告。

```yaml
type: hero
palette: elegant
rendering: digital
mood: subtle
font: serif
```

**Prompt hints**:
- Off-white background (#FAFAFA)
- Deep purple accents (#553C9A)
- Clean lines, professional layout
- Elegant typography

### announcement-bold

醒目公告风，适合产品发布和活动公告。

```yaml
type: hero
palette: vivid
rendering: flat-vector
mood: bold
font: display
```

**Prompt hints**:
- White or vibrant background
- Bold primary colors
- Dynamic shapes, high contrast
- Large impactful title

### minimal-zen

极简禅意风，适合哲学思考和核心概念。

```yaml
type: minimal
palette: mono
rendering: flat-vector
mood: subtle
font: clean
```

**Prompt hints**:
- Pure white background (#FFFFFF)
- Black or dark gray accents
- Single focal element
- Maximum whitespace (60%+)

### creative-playful

创意童趣风，适合创意内容和轻松话题。

```yaml
type: metaphor
palette: pastel
rendering: hand-drawn
mood: balanced
font: handwritten
```

**Prompt hints**:
- Light pink/cream background
- Soft pastel colors
- Playful doodles, organic lines
- Friendly, whimsical feel

### retro-vintage

复古怀旧风，适合历史内容和怀旧话题。

```yaml
type: scene
palette: retro
rendering: painterly
mood: subtle
font: serif
```

**Prompt hints**:
- Sepia-toned background
- Burnt orange, mustard colors
- Vintage textures, grain overlay
- Classic typography

## Usage

```bash
# Using preset
/cover-image article.md --style tech-dark

# Preset with custom aspect
/cover-image article.md --style announcement-bold --aspect 2.35:1

# Override preset dimensions
/cover-image article.md --style tech-dark --palette cool
```

## Custom Presets

Users can create custom presets by adding to their EXTEND.md:

```yaml
style_presets:
  my-brand:
    type: hero
    palette: elegant
    rendering: digital
    mood: subtle
    font: clean
    custom_prompt_hints: |
      Use brand colors: primary #FF6B35, background #1A1A2E
      Include subtle brand pattern in background
```
