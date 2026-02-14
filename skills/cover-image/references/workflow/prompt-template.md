# Step 3: Prompt Template

Save to `prompts/cover.md`:

```markdown
---
type: cover
palette: [confirmed palette]
rendering: [confirmed rendering]
references:
  - ref_id: 01
    filename: refs/ref-01-{slug}.{ext}
    usage: direct | style | palette
---

# Content Context
Article title: [full original title from source]
Content summary: [2-3 sentence summary of key points and themes]
Keywords: [5-8 key terms extracted from content]

# Visual Design
Cover theme: [2-3 words visual interpretation]
Type: [confirmed type]
Palette: [confirmed palette]
Rendering: [confirmed rendering]
Font: [confirmed font]
Text level: [confirmed text level]
Mood: [confirmed mood]
Aspect ratio: [confirmed ratio]
Language: [confirmed language]

# Text Elements
[Based on text level:]
- none: "No text elements"
- title-only: "Title: [exact title from source or user]"
- title-subtitle: "Title: [title] / Subtitle: [context]"
- text-rich: "Title: [title] / Subtitle: [context] / Tags: [2-4 keywords]"

# Mood Application
[Based on mood level:]
- subtle: "Use low contrast, muted colors, light visual weight, calm aesthetic"
- balanced: "Use medium contrast, normal saturation, balanced visual weight"
- bold: "Use high contrast, vivid saturated colors, heavy visual weight, dynamic energy"

# Font Application
[Based on font style:]
- clean: "Use clean geometric sans-serif typography. Modern, minimal letterforms."
- handwritten: "Use warm hand-lettered typography with organic brush strokes. Friendly, personal feel."
- serif: "Use elegant serif typography with refined letterforms. Classic, editorial character."
- display: "Use bold decorative display typography. Heavy, expressive headlines."

# Composition
Type composition:
- [Type-specific layout and structure]

Visual composition:
- Main visual: [metaphor derived from content meaning]
- Layout: [positioning based on type and aspect ratio]
- Decorative: [palette-specific elements that reinforce content theme]

Color scheme: [primary, background, accent from palette definition, adjusted by mood]
Rendering notes: [key characteristics from rendering definition]
Type notes: [key characteristics from type definition]
Palette notes: [key characteristics from palette definition]

[Reference images section if provided]
```

## Reference-Driven Design

When reference images are provided, they are the **primary visual input** and MUST strongly influence the output.

**Passing `--ref` alone is NOT enough.** Image generation models often ignore reference images unless the prompt text explicitly describes what to reproduce. Always combine `--ref` with detailed textual instructions.

## Type-Specific Composition

| Type | Composition Guidelines |
|------|------------------------|
| `hero` | Large focal visual (60-70% area), title overlay on visual, dramatic composition |
| `conceptual` | Abstract shapes representing core concepts, information hierarchy, clean zones |
| `typography` | Title as primary element (40%+ area), minimal supporting visuals, strong hierarchy |
| `metaphor` | Concrete object/scene representing abstract idea, symbolic elements, emotional resonance |
| `scene` | Atmospheric environment, narrative elements, mood-setting lighting and colors |
| `minimal` | Single focal element, generous whitespace (60%+), essential shapes only |

## Title Guidelines

When text level includes title:
- **Source**: Use the exact title provided by user, or extract from source content
- **Do NOT invent titles**: Stay faithful to the original
- Match confirmed language

## Reference Image Handling

When user provides reference images (`--ref` or pasted images):

### Reference Analysis Template

| Aspect | Analysis Points |
|--------|-----------------|
| **Brand elements** | Logos, wordmarks, distinctive typography |
| **Signature patterns** | Unique motifs, textures, geometric patterns |
| **Colors** | Exact hex values or close approximations |
| **Layout** | Spatial zones, banner placement, proportions |
| **Typography** | Font style, weight, case, spacing, position |
| **Rendering** | Line quality, texture, depth treatment |
| **Elements** | Icon vocabulary, decorative motifs |

**Output**: Each extracted element should be written as a **copy-pasteable prompt instruction** prefixed with "MUST" or "REQUIRED".
