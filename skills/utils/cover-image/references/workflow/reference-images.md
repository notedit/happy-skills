# Reference Images Workflow

## Step 1: Save Reference Images

When user provides reference images, save them systematically:

```
<output-dir>/refs/
├── ref-01-{slug}.{ext}      # Reference image file
├── ref-01-{slug}.md         # Analysis/notes file
├── ref-02-{slug}.{ext}
├── ref-02-{slug}.md
└── ...
```

### Naming Convention

- `ref-NN`: Sequential number (01, 02, 03...)
- `{slug}`: 2-4 word kebab-case describing the reference
- `{ext}`: Original file extension (png, jpg, etc.)

## Step 2: Analyze Reference Images

For each reference image, extract:

| Aspect | What to Extract |
|--------|-----------------|
| **Style** | Rendering technique, line quality, texture |
| **Composition** | Layout, visual hierarchy, focal points |
| **Color mood** | Palette characteristics |
| **Elements** | Key visual elements and symbols used |
| **Typography** | Font style, treatment (if applicable) |
| **Mood** | Emotional tone and visual weight |

## Step 3: Generate Analysis File

Create a `.md` file for each reference with analysis:

```markdown
# Reference 01: [name]

## Visual Style
- Rendering: [flat-vector/hand-drawn/etc.]
- Line quality: [description]
- Texture: [description]

## Composition
- Layout: [description]
- Focal point: [description]
- Whitespace: [percentage/feel]

## Colors
- Primary: [hex values]
- Secondary: [hex values]
- Background: [hex values]

## Elements
- [List of visual elements]

## Integration Notes
- [How to use this reference in generation]
```

## Step 4: Add to Prompt Frontmatter

When reference files are saved, add to prompt frontmatter:

```yaml
---
type: cover
palette: warm
rendering: flat-vector
references:
  - ref_id: 01
    filename: refs/ref-01-style-reference.png
    usage: style
  - ref_id: 02
    filename: refs/ref-02-color-reference.jpg
    usage: palette
---
```

### Usage Types

| Usage | When to Use | Generation Action |
|-------|-------------|-------------------|
| `direct` | Reference matches desired output closely | Pass reference image directly to generation |
| `style` | Extract visual style characteristics only | Describe style in prompt text |
| `palette` | Extract color palette only | Include colors in prompt |

## Step 5: Embed in Prompt Body

**CRITICAL**: Passing `--ref` alone is NOT enough. You MUST write detailed textual instructions.

```
# Reference Style -- MUST INCORPORATE

CRITICAL: The generated cover MUST visually reference the provided images.

## From Ref 1 ([filename]) -- REQUIRED elements:
- [Brand element]: [Specific description]
- [Signature pattern]: [Specific description]
- [Colors]: [Exact hex values]
- [Typography]: [Specific treatment]
- [Layout element]: [Specific spatial element]

## Integration approach:
[Specific layout instruction describing how reference elements combine]
```

## Guidelines

- Each visual element gets its own bullet with "MUST" or "REQUIRED"
- Descriptions must be **specific enough to reproduce**
- The integration approach must describe **exact spatial arrangement**
- After generation, verify reference elements are visible; if not, strengthen and regenerate
