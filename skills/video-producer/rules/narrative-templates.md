---
name: narrative-templates
description: Reusable narrative structures for common video types with scene slot definitions
metadata:
  tags: video, narrative, template, scenes, remotion, promo
---

## Template Selection

| Video Type | Template | Duration | Scenes | Best For |
|-----------|----------|----------|--------|----------|
| Product promo / SaaS ad | SaaS Product Promo | 22-30s | 8 | Landing page hero, product launch, feature demo |
| Text-driven / quote video | Typographic Promo | 18-25s | 7 | Brand manifesto, statement video, inspirational |
| Transparent overlay | Social Media Overlay | 4-6s | 1 | Compositing in video editors, streaming |

---

## 1. SaaS Product Promo (22-30s, 8 scenes)

**Narrative arc:** Hook → Question → Reveal → Benefit → Comparison → Demo → Showcase → CTA

This is the most common structure. Every scene serves a specific persuasion function.

| # | Scene | Duration | Purpose | Recommended Pattern | Content Slot |
|---|-------|----------|---------|--------------------|----|
| 1 | Hook | 2-3s | Grab attention, state the premise | TitleCard + PerspectiveEntrance | Product name + bold claim |
| 2 | Question | 2-3s | Present the pain point | CardFlip3D | Pain on front → solution tease on back |
| 3 | Brand Reveal | 2-3s | Introduce the product | charCascade effect | "Meet [Product Name]" |
| 4 | Core Benefit | 3-4s | Show the key value prop | SplitScreenComparison | Old way vs new way |
| 5 | Comparison | 3-4s | Make the winner clear | SplitScreenComparison (dimLeft) | Left dims → right pops |
| 6 | Feature Demo | 3-4s | Show product in action | CursorClick | Simulated UI interaction |
| 7 | Showcase | 3-4s | Social proof / variety | Remotion native grid | Feature grid or screenshot montage |
| 8 | CTA | 2-3s | Call to action | Outro + CursorClick | Tagline + button click simulation |

**Transitions:** `circleReveal` or `wipeIn` between scenes. Use TransitionSeries with `fade()` or `slide()` for simpler videos.

**Background:** Single FluidBackground component spanning all scenes (see style presets).

**Scene 1 detail — Hook:**
Two-phase scene. Phase 1 (first 60%): Product name + bold claim with perspective entrance from both sides. Phase 2 (last 40%): Content rotates backward (rotateX exit), new text falls in — the "but" statement introducing the problem.

**Scene 2 detail — Question:**
Large card centered, front shows the "old way" (terminal/code), back shows the "new way" (clean UI). Card flips via 3D rotateY at ~40% through the scene. Front face has dark background, back face has glassmorphism.

**Scene 4-5 detail — Comparison:**
Scene 4 shows both panels equally. Scene 5 reuses the layout but applies dimLeft: left panel gets opacity:0.5 + blur(4px), right panel scales to 1.02. This creates a clear visual "winner".

**Scene 6 detail — Feature Demo:**
Show a simplified UI mockup (input field, chat interface, or dashboard). Cursor slides in from off-screen, clicks the primary action. Target element depresses (scale:0.95) then releases. Ripple expands from click point.

**Scene 7 detail — Showcase:**
Grid of cards (3x3 or 4x2) with staggered pop-in entrance. Each card has a gradient top half + label bottom half. Grid slowly scrolls diagonally. After 30% of scene, overlay text appears and grid blurs behind it.

**Scene 8 detail — CTA:**
Brand name in large type (typewriter effect optional). Tagline fades in below. After 60% of scene, cursor slides to CTA button and clicks. End on the ripple expanding.

---

## 2. Typographic Promo (18-25s, 7 scenes)

**Narrative arc:** Statement → Break → Statement → Break → Statement → Break → Closing

Pure typography and color. No product UI or mockups. Each text scene delivers one key message with visual emphasis through highlight boxes.

| # | Scene | Duration | Purpose | Recommended Pattern | Content Slot |
|---|-------|----------|---------|--------------------|----|
| 1 | Opening | 2-3s | First powerful statement | TitleCard or TextHighlightBox | Opening quote or hook |
| 2 | Visual Break A | 1-2s | Visual breathing room | PerspectiveEntrance or full-screen image | Abstract shape, icon, or footage |
| 3 | Statement B | 2-3s | Second key message | TextHighlightBox | Message with highlighted keywords |
| 4 | Visual Break B | 1-2s | Contrast moment | CardFlip3D or full-screen image | Visual reveal on flip |
| 5 | Statement C | 2-3s | Third key message | RotateXTextSwap | Swap between contrasting ideas |
| 6 | Visual Break C | 1-2s | Final visual | Full-screen image or shape | Transition to closing |
| 7 | Closing | 2-3s | Brand + tagline | Outro | Brand name + tagline |

**Typography rules (critical):**
- Unified font size: 72-96px across all text scenes
- Line height: 0.8 (extremely tight, text block feels solid)
- Max width: 70% of viewport
- Center-aligned, vertically centered
- Font weight: 800-900 (heavy geometric sans-serif)

**Highlight boxes:**
Colored rectangles (scaleX: 0→1) behind specific words. Use 2 colors max — one primary, one accent. Highlight the most important word in each statement.

**Visual breaks:**
Can be full-screen placeholder images (cityscape, nature, architecture) or abstract animation (PerspectiveEntrance with geometric shapes). Keep under 2 seconds — they're rhythm, not content.

---

## 3. Social Media Overlay (4-6s, transparent background)

Single scene with a multi-step animation sequence. Rendered with alpha channel for compositing in video editors.

| Step | Timing | Animation | Ease |
|------|--------|-----------|------|
| 1. Cards pop in | 0-0.6s | `from { scale: 0, opacity: 0 }`, stagger 0.1s | `back.out(2)` |
| 2. Bars extend | 0.4-0.9s | `from { scaleX: 0, transformOrigin: 'left' }` | `power2.out` |
| 3. Text fade in | 0.7-1.0s | `from { opacity: 0, y: 10 }` | `power2.out` |
| 4. Hold | 1.0-4.0s | Static display | — |
| 5. Reverse exit | 4.0-5.0s | Reverse entrance sequence | `power2.in` |

**Layout patterns:**
- Follow cards: 2-column grid (3+3), 80px horizontal gap, 32px vertical gap
- Stat cards: Single row, centered
- Lower third: Bottom-aligned bar

**Rendering:** Must use ProRes 4444 (.mov) or WebM VP9 (.webm) for alpha channel. MP4 does NOT support transparency.

---

## Duration Calculator

```
total_frames = sum(scene_frames) + (num_transitions * transition_frames)
scene_frames = ceil(scene_seconds * fps)
transition_frames = 15  (standard fade/slide)
```

Example for SaaS Promo at 30fps:
```
Scene 1: 3.0s = 90 frames
Scene 2: 3.0s = 90 frames
Scene 3: 2.5s = 75 frames
Scene 4: 3.5s = 105 frames
Scene 5: 3.0s = 90 frames
Scene 6: 3.5s = 105 frames
Scene 7: 3.5s = 105 frames
Scene 8: 3.0s = 90 frames
Transitions: 7 × 15 = 105 frames
Total: 855 frames = 28.5s
```
