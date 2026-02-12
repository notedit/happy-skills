---
name: style-presets
description: Visual style presets with complete color, typography, and animation specifications
metadata:
  tags: video, style, design, colors, typography, presets
---

## Preset Selection

| Preset | Vibe | Background | Best For |
|--------|------|------------|----------|
| Apple Minimal | Clean, premium, soft | Fluid gradient | SaaS promo, product launch |
| Bold Typography | High-impact, editorial | Solid white or black | Quote videos, brand manifesto |
| Dark Tech | Futuristic, developer | Deep navy/black | Dev tools, API products, tech |

---

## 1. Apple Minimal

The "safe default". Inspired by Apple keynote aesthetics — soft gradients, generous whitespace, smooth spring physics.

### Colors
```ts
const COLORS = {
  background: '#FFF5F0',           // Warm cream white
  textPrimary: '#1A1A1A',          // Near-black
  textSecondary: '#6B7280',        // Muted gray
  accent: '#FF7D00',               // Warm orange (swap per brand)
  accentLight: 'rgba(255,125,0,0.15)',
  surface: 'rgba(255,255,255,0.65)',       // Glass panels
  surfaceDark: '#1E1E2E',                  // Code/terminal bg
  gradientBlobA: '#FFD1C1',        // Background blob
  gradientBlobB: '#E0C3FC',        // Background blob
};
```

### Typography
```ts
const TYPOGRAPHY = {
  fontFamily: 'Inter, system-ui, sans-serif',
  heroSize: 90,       // Scene titles
  titleSize: 64,      // Subtitles
  bodySize: 32,       // Body text
  labelSize: 18,      // Captions
  weight: { bold: 700, extraBold: 800 },
};
```

### Animation
- All entrances: `spring({ damping: 12-15, stiffness: 120-150 })`
- All exits: `interpolate()` with `extrapolateRight: 'clamp'`
- No linear animations — everything uses spring or ease curves
- Overlap animations with 0.3-0.5s for fluid sequencing

### Surfaces
- Glass panels: `background: rgba(255,255,255,0.6)`, `backdropFilter: blur(20px)`, `borderRadius: 16-24px`
- Dark panels: `background: #1E1E2E`, `borderRadius: 16-24px`, deep shadow
- Card shadow: `boxShadow: '0 50px 120px rgba(0,0,0,0.15)'`

### Background
FluidBackground with 2-3 blurred color blobs drifting slowly. Colors match `gradientBlobA` and `gradientBlobB`.

---

## 2. Bold Typography

Maximum visual impact through text alone. No UI mockups, no glass panels — pure typography and strategic color highlights.

### Colors
```ts
const COLORS = {
  background: '#FFFFFF',           // Pure white
  textPrimary: '#0F172A',          // Dark navy
  highlightA: '#CCFF00',           // Neon green
  highlightB: '#FF0066',           // Hot pink
};
```

For dark variant:
```ts
const COLORS = {
  background: '#0F172A',           // Dark navy
  textPrimary: '#FFFFFF',          // White
  highlightA: '#CCFF00',           // Neon green
  highlightB: '#FF0066',           // Hot pink
};
```

### Typography
```ts
const TYPOGRAPHY = {
  fontFamily: '"Eina Bold", "Inter Black", "Montserrat Black", system-ui',
  fontSize: 80,           // UNIFIED across all text scenes
  lineHeight: 0.8,        // Extremely tight — text block feels solid
  maxWidth: '70%',        // of viewport width
  weight: { primary: 900 },
  textTransform: 'uppercase',
};
```

**Critical rules:**
- ONE font size for all text scenes (72-96px range)
- Line height 0.8 — tighter than standard
- Text container always 70% viewport width, centered
- All caps for maximum impact
- No font size variation between scenes

### Animation
- Text: slide up from below + opacity fade, using `spring()`
- Highlight boxes: `scaleX: 0 → 1`, appearing AFTER text stops moving
- Highlight boxes sit at lower z-index behind text
- Transitions between text and visual breaks: hard cuts (no fade)

### Highlight Boxes
```tsx
// Colored rectangle scaling in behind a word
<div style={{
  position: 'absolute',
  background: COLORS.highlightA,  // or highlightB
  zIndex: -1,
  transformOrigin: 'left center',
  transform: `scaleX(${highlightProgress})`,
  // Position derived from word element's offsetLeft/offsetTop
}} />
```

Use max 2 highlight colors per video. Alternate between them.

### Background
Solid color only. No gradients, no blobs, no visual noise.

---

## 3. Dark Tech

Developer-focused, futuristic aesthetic. Neon accents against deep dark backgrounds. Terminal/code mockups are first-class citizens.

### Colors
```ts
const COLORS = {
  background: '#0F172A',           // Deep navy
  textPrimary: '#FFFFFF',          // White
  textSecondary: '#94A3B8',        // Slate gray
  accent: '#3B82F6',               // Electric blue
  accentAlt: '#8B5CF6',            // Purple
  codeGreen: '#4ADE80',            // Terminal green
  codeGray: '#6B7280',             // Terminal comments
  surface: 'rgba(30, 41, 59, 0.8)',       // Dark glass
  border: 'rgba(148, 163, 184, 0.2)',     // Subtle borders
};
```

### Typography
```ts
const TYPOGRAPHY = {
  fontFamily: 'Inter, system-ui, sans-serif',
  monoFamily: '"JetBrains Mono", "Fira Code", "SF Mono", monospace',
  heroSize: 80,
  titleSize: 56,
  bodySize: 28,
  codeSize: 20,
  weight: { bold: 700, extraBold: 800 },
};
```

### Animation
- Entrances: GSAP timeline orchestration for complex sequences
- Text: charCascade with `back.out(1.7)` for tech feel
- Transitions: `circleReveal` or `wipeIn`
- Subtle glow effects on accent elements: `boxShadow: '0 0 30px rgba(59,130,246,0.3)'`

### Surfaces
- Code windows: `background: #1A1A2E`, monospace font, colored syntax
- Browser mockups: Dark chrome with 3 dots (traffic lights)
- Cards: `background: rgba(30,41,59,0.8)`, `border: 1px solid rgba(148,163,184,0.2)`, `borderRadius: 12px`

### Background
Solid dark (#0F172A). Optional: very slow-moving subtle gradient blobs at 10-15% opacity for depth. Or use react-animation Aurora with dark color stops.

---

## Selecting a Preset

| User says... | Preset |
|-------------|--------|
| "Apple style", "clean", "premium", "soft" | Apple Minimal |
| "bold text", "typography", "editorial", "impactful" | Bold Typography |
| "dark mode", "developer", "tech", "futuristic" | Dark Tech |
| "professional", "corporate", no preference | Apple Minimal (default) |

Mix is possible but not recommended. If user wants both dark background AND bold typography, use Dark Tech with increased font sizes.
