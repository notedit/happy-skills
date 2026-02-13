---
name: style-presets
description: Visual style presets with complete color, typography, and animation specifications
metadata:
  tags: video, style, design, colors, typography, presets
---

## NEVER — Anti-Pattern Blacklist

These are the hallmarks of generic, forgettable "AI slop" videos. Avoid them at all costs.

**Typography:**
- NEVER use Inter, Roboto, Arial, Helvetica, or system-ui as your display/hero font
- NEVER use Montserrat, Poppins, or Nunito — they are overused and signal "template"
- NEVER use the same font for every video — rotate display fonts across productions
- NEVER default to center-aligned text for everything — try left-anchored, right-anchored, or diagonal

**Color:**
- NEVER use purple-to-blue gradients on white backgrounds — this is the #1 "AI generated" signal
- NEVER use evenly-distributed pastel palettes where no color dominates
- NEVER pick "safe" blues (#3B82F6, #6366F1) as your only accent — be bolder
- NEVER use the same accent color across consecutive videos

**Motion:**
- NEVER fade-in every element with the same timing — use staggered delays or varied entrances
- NEVER use uniform 0.3s fade for all transitions — vary timing based on scene purpose
- NEVER apply the same entrance animation to every text block — differentiate hero text from body text
- NEVER skip the memory anchor — at least one scene must have 2x the animation investment

**Composition:**
- NEVER center everything symmetrically in every scene — break the grid at least once
- NEVER use identical padding/margins across all scenes — create visual rhythm through variety
- NEVER use pure white or pure black backgrounds without texture or atmosphere

**General:**
- NEVER produce a video that could be mistaken for a Canva template
- NEVER let the "safe default" win — if it feels generic, push further

---

## Preset Selection

| Preset | Vibe | Background | Best For |
|--------|------|------------|----------|
| Apple Minimal | Clean, premium, soft | Fluid gradient | SaaS promo, product launch |
| Bold Typography | High-impact, editorial | Solid white or black | Quote videos, brand manifesto |
| Dark Tech | Futuristic, developer | Deep navy/black | Dev tools, API products, tech |
| Warm Organic | Natural, approachable, human | Soft texture/grain | Health, wellness, lifestyle, education |
| Retro Pop | Vibrant, nostalgic, bold | Geometric patterns | Consumer apps, social media, entertainment |
| Editorial Mono | Refined, magazine, intellectual | Off-white/charcoal | Finance, media, luxury, B2B |

---

## 1. Apple Minimal

Premium keynote aesthetics — soft gradients, generous whitespace, smooth spring physics.

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
  fontFamily: '"SF Pro Display", "Satoshi", "General Sans", sans-serif',
  heroSize: 90,       // Scene titles
  titleSize: 64,      // Subtitles
  bodySize: 32,       // Body text
  labelSize: 18,      // Captions
  weight: { bold: 700, extraBold: 800 },
};
```

### Animation (Spring Presets)
- Primary entrance: `SPRING.snappy` — clean, minimal bounce
- Stagger: 5-6 frames between elements
- Exits: `SPRING.smooth` via `useSpringEnterExit`
- Transitions: `SpringCrossfade` with `SPRING.smooth`
- No linear animations — everything uses spring physics
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
  fontFamily: '"Clash Display", "Cabinet Grotesk", "Darker Grotesque", sans-serif',
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

### Animation (Spring Presets)
- Primary entrance: `SPRING.stiff` — fast, minimal bounce for impact
- Text: `WordTrail` or `CharacterTrail` with `SPRING.stiff`, stagger 2-3 frames
- Highlight boxes: `scaleX: 0 → 1` via GSAP (needs SplitText for word positioning)
- Transitions between text and visual breaks: hard cuts (no fade, no spring)

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
  fontFamily: '"Geist", "Outfit", "Switzer", sans-serif',
  monoFamily: '"JetBrains Mono", "Fira Code", "Berkeley Mono", monospace',
  heroSize: 80,
  titleSize: 56,
  bodySize: 28,
  codeSize: 20,
  weight: { bold: 700, extraBold: 800 },
};
```

### Animation (Spring Presets)
- Primary entrance: `SPRING.snappy` or `SPRING.stiff` — precise, technical feel
- Stagger: 3-4 frames (fast, data-like)
- Text: GSAP `charCascade` for char-level effects, or `CharacterTrail` with `SPRING.stiff` for simpler scenes
- Transitions: `circleReveal` or `wipeIn` (GSAP) for cinematic; `SpringSlide` for quicker scenes
- Subtle glow effects on accent elements: `boxShadow: '0 0 30px rgba(59,130,246,0.3)'`

### Surfaces
- Code windows: `background: #1A1A2E`, monospace font, colored syntax
- Browser mockups: Dark chrome with 3 dots (traffic lights)
- Cards: `background: rgba(30,41,59,0.8)`, `border: 1px solid rgba(148,163,184,0.2)`, `borderRadius: 12px`

### Background
Solid dark (#0F172A). Optional: very slow-moving subtle gradient blobs at 10-15% opacity for depth. Or use react-animation Aurora with dark color stops.

---

## 4. Warm Organic

Natural, human, approachable. Inspired by wellness brands, educational platforms, and lifestyle products. Rounded shapes, warm tones, and gentle motion.

### Colors
```ts
const COLORS = {
  background: '#FDF6EC',           // Warm parchment
  textPrimary: '#2D2418',          // Dark brown
  textSecondary: '#8B7355',        // Warm taupe
  accent: '#D4764E',               // Terracotta
  accentLight: 'rgba(212,118,78,0.15)',
  secondary: '#7BA68D',            // Sage green
  surface: 'rgba(253,246,236,0.85)',      // Warm glass
  gradientBlobA: '#F5D6C3',        // Peach blob
  gradientBlobB: '#D4E8DA',        // Mint blob
};
```

### Typography
```ts
const TYPOGRAPHY = {
  displayFamily: '"Fraunces", "Playfair Display", serif',    // Serif for headlines
  bodyFamily: '"DM Sans", "Plus Jakarta Sans", sans-serif',  // Clean sans for body
  heroSize: 84,
  titleSize: 56,
  bodySize: 30,
  labelSize: 16,
  weight: { display: 700, body: 400, bodyBold: 600 },
};
```

**Key rule:** Serif display + sans-serif body pairing creates warmth with readability.

### Animation (Spring Presets)
- Primary entrance: `SPRING.gentle` — slow, dreamy, organic
- Alt entrance: `SPRING.molasses` for extra weight on hero elements
- Stagger: 6-8 frames (slow, deliberate)
- Reveals: gentle scale from 0.95 → 1.0 via spring with `overshootClamping: true`
- Transitions: `SpringCrossfade` with `SPRING.gentle` — no sharp cuts ever
- **No GSAP needed** for most scenes — spring-only produces the best warm feel

### Surfaces
- Rounded cards: `borderRadius: 24-32px`, soft shadow, warm tint
- No sharp corners — everything 16px radius minimum
- Subtle grain texture overlay at 3-5% opacity for organic feel

### Background
Soft gradient with warm blobs. Add react-animation NoiseOverlay at low opacity (0.03-0.05) for paper-like texture.

---

## 5. Retro Pop

Vibrant, nostalgic, unapologetically bold. Inspired by 90s design, Memphis style, and pop art. Geometric shapes, high saturation, playful layout breaks.

### Colors
```ts
const COLORS = {
  background: '#FFFBE6',           // Warm cream
  textPrimary: '#1A1A1A',          // Black
  accent: '#FF5733',               // Hot red-orange
  secondary: '#FFC300',            // Bright yellow
  tertiary: '#6C63FF',             // Electric violet
  surface: '#FF5733',              // Accent surface
  shadow: 'rgba(26,26,26,0.2)',
};
```

For dark variant:
```ts
const COLORS = {
  background: '#1A1A2E',           // Deep purple-black
  textPrimary: '#FFFBE6',          // Cream
  accent: '#FF5733',               // Hot red-orange
  secondary: '#FFC300',            // Bright yellow
  tertiary: '#00D9FF',             // Cyan
};
```

### Typography
```ts
const TYPOGRAPHY = {
  displayFamily: '"Familjen Grotesk", "Space Grotesk", "Archivo Black", sans-serif',
  bodyFamily: '"Spline Sans", "Instrument Sans", sans-serif',
  heroSize: 96,          // Extra large
  titleSize: 64,
  bodySize: 28,
  weight: { display: 900, body: 500 },
  textTransform: 'uppercase',      // Headers only
};
```

**Key rule:** Allow mixed-case body text but UPPERCASE display text. Maximum contrast between headline and body.

### Animation (Spring Presets)
- Primary entrance: `SPRING.pop` or `SPRING.rubber` — maximum overshoot
- Alt entrance: `SPRING.wobbly` for elastic wobble
- Stagger: 2-3 frames (rapid-fire pop-ins)
- Grid reveals: `GridStagger` center-out with `SPRING.pop`
- Geometric shapes: independent spring animations with random delays
- Transitions: hard cuts with flash frames (2-frame white flash)
- **Spring-dominant:** Most scenes use spring-only; GSAP only for ScrambleText decode effects

### Decorative Elements
```tsx
// Floating geometric shapes behind/around content
<div style={{
  position: 'absolute',
  width: 120, height: 120,
  background: COLORS.secondary,
  borderRadius: shape === 'circle' ? '50%' : shape === 'diamond' ? '0' : '16px',
  transform: `rotate(${rotation}deg) scale(${scale})`,
  zIndex: -1,
}} />
```

Scatter 3-5 geometric shapes per scene. Rotate slowly. Colors from palette.

### Background
Solid warm cream or use geometric pattern (dots grid, diagonal stripes at 5% opacity). NEVER gradient blobs — that's Apple Minimal territory.

---

## 6. Editorial Mono

Refined, intellectual, magazine-inspired. Monochromatic with one strategic accent. Grid-heavy layouts with deliberate asymmetry. Inspired by Monocle, Bloomberg, and high-end print design.

### Colors
```ts
const COLORS = {
  background: '#F5F1EB',           // Warm off-white
  textPrimary: '#1C1917',          // Rich black
  textSecondary: '#78716C',        // Stone gray
  accent: '#DC2626',               // Single red accent (used sparingly)
  rule: '#D6D3D1',                 // Divider lines
  surface: '#FFFFFF',              // Card surfaces
};
```

For dark variant:
```ts
const COLORS = {
  background: '#1C1917',           // Rich black
  textPrimary: '#F5F1EB',          // Warm off-white
  textSecondary: '#A8A29E',        // Stone gray
  accent: '#EF4444',               // Red accent
  rule: '#44403C',                 // Divider lines
  surface: '#292524',              // Card surfaces
};
```

### Typography
```ts
const TYPOGRAPHY = {
  displayFamily: '"Newsreader", "Source Serif 4", "Crimson Pro", serif',
  bodyFamily: '"Instrument Sans", "IBM Plex Sans", sans-serif',
  monoFamily: '"IBM Plex Mono", "Inconsolata", monospace',
  heroSize: 72,
  titleSize: 48,
  bodySize: 24,
  captionSize: 14,
  weight: { display: 600, body: 400, label: 500 },
  letterSpacing: { display: '-0.02em', label: '0.12em' },
};
```

**Key rules:**
- Serif headlines + sans-serif body — always
- UPPERCASE small labels with wide letter-spacing (`0.12em`)
- Generous line-height (1.3-1.5) for readability
- Use thin horizontal rules (`1px solid`) as scene dividers

### Animation (Spring Presets)
- Primary entrance: `SPRING.smooth` — near-zero overshoot, refined motion
- Alt entrance: `SPRING.gentle` for large display numbers or pull-quotes
- Stagger: 8-10 frames (deliberate, unhurried)
- Entrances: opacity 0→1 with slight translateY (20px max) via spring
- Hold times: LONGER than other presets (1.5-2s per text block)
- Transitions: `SpringCrossfade` with `SPRING.smooth`, 20-frame duration (slower)
- The accent color appears via a single animated underline or dot — never splashed everywhere
- **No GSAP needed** — the restraint of this preset means spring-only is ideal
- Motion should feel like turning a magazine page — smooth, quiet, purposeful

### Layout
- Asymmetric grid: text at 1/3 or 2/3 horizontal position, never centered
- Horizontal rules between content sections
- Large numbers (statistics, dates) set in display serif at 120px+
- Pull-quote style: oversized quotation marks in accent color

### Background
Off-white or charcoal. No effects, no gradients, no texture. The paper IS the design.

---

## Selecting a Preset

| User says... | Preset |
|-------------|--------|
| "Apple style", "clean", "premium", "soft" | Apple Minimal |
| "bold text", "typography", "editorial text-only", "impactful" | Bold Typography |
| "dark mode", "developer", "tech", "futuristic" | Dark Tech |
| "warm", "organic", "natural", "friendly", "wellness" | Warm Organic |
| "fun", "bold colors", "retro", "playful", "vibrant" | Retro Pop |
| "refined", "magazine", "intellectual", "monochrome" | Editorial Mono |
| "professional", "corporate", no preference | Apple Minimal (default) |

Mix is possible but not recommended. If user wants both dark background AND bold typography, use Dark Tech with increased font sizes.

---

## Creative Typography Guide

Typography is the fastest signal of quality. A distinctive font choice elevates the entire video instantly.

### Display Fonts by Mood

| Mood | Recommended Fonts | Avoid |
|------|-------------------|-------|
| Premium / Clean | Satoshi, General Sans, Switzer | Inter, Roboto |
| Bold / Impact | Clash Display, Cabinet Grotesk, Darker Grotesque | Montserrat, Poppins |
| Tech / Modern | Geist, Outfit, Space Grotesk, Familjen Grotesk | Arial, Helvetica |
| Warm / Human | Fraunces, Playfair Display, DM Serif Display | Times New Roman |
| Editorial / Refined | Newsreader, Source Serif 4, Crimson Pro | Georgia |
| Playful / Fun | Fredoka, Bricolage Grotesque, Rubik | Comic Sans, Nunito |

### Pairing Principles

1. **Contrast > Harmony:** Pair a serif display with a sans-serif body, or a heavy grotesque with a light humanist
2. **One hero font:** The display font carries personality. The body font should be invisible (high readability, low character)
3. **Weight contrast:** Display at 700-900, body at 400-500. Never both at the same weight
4. **Size ratio:** Display should be 2.5-4x the body size. Timid ratios (1.5x) feel generic

### Monospace for Accent

Use monospace fonts (`JetBrains Mono`, `Berkeley Mono`, `IBM Plex Mono`) as accent typography — not just for code. Monospace at small sizes with wide letter-spacing creates a distinctive label/caption style that works across all presets.
