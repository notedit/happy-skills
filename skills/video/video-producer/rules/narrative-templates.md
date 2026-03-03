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

| # | Scene | Duration | Purpose | Default Pattern (Spring) | GSAP Alternative | Content Slot |
|---|-------|----------|---------|-------------------------|-------------------|---|
| 1 | Hook | 2-3s | Grab attention, state the premise | SpringEntrance + WordTrail | TitleCard + PerspectiveEntrance | Product name + bold claim |
| 2 | Question | 2-3s | Present the pain point | SpringCardFlip | CardFlip3D | Pain on front → solution tease on back |
| 3 | Brand Reveal | 2-3s | Introduce the product | CharacterTrail (SPRING.bouncy) | charCascade effect | "Meet [Product Name]" |
| 4 | Core Benefit | 3-4s | Show the key value prop | SpringTrail side-by-side | SplitScreenComparison | Old way vs new way |
| 5 | Comparison | 3-4s | Make the winner clear | Spring opacity+scale shift | SplitScreenComparison (dimLeft) | Left dims → right pops |
| 6 | Feature Demo | 3-4s | Show product in action | ScalePop UI elements | CursorClick | Simulated UI interaction |
| 7 | Showcase | 3-4s | Social proof / variety | GridStagger (SPRING.pop) | Remotion native grid | Feature grid or screenshot montage |
| 8 | CTA | 2-3s | Call to action | SpringOutro | Outro + CursorClick | Tagline + button click simulation |

**Spring-first rule:** Default to the Spring column. Use the GSAP Alternative only when you need SplitText char masking, DrawSVG, or complex timeline labels.

**Transitions:** `SpringCrossfade` or `SpringSlide` between scenes (default). Use `circleReveal` or `wipeIn` (GSAP) for cinematic effect. Use TransitionSeries with `fade()` or `slide()` for simple linear transitions.

**Background:** Single FluidBackground component spanning all scenes (see style presets).

**Scene 1 detail — Hook:**
Two-phase scene. **Spring version:** Phase 1 — product name + bold claim enter from sides via `spring({ config: SPRING.bouncy })` with `interpolate(entrance, [0,1], [-600, 0])`. Phase 2 — first text exits with `SPRING.stiff`, new text springs in with `SPRING.pop`. **GSAP version:** Phase 1 — PerspectiveEntrance with rotateY from both sides. Phase 2 — rotateX exit, new text falls in.

**Scene 2 detail — Question:**
Large card centered, front shows the "old way" (terminal/code), back shows the "new way" (clean UI). **Spring version:** SpringCardFlip — spring-driven 3D rotateY at ~40% through scene, natural bounce on landing. **GSAP version:** CardFlip3D with precise timeline control. Front face has dark background, back face has glassmorphism.

**Scene 4-5 detail — Comparison:**
Scene 4 shows both panels equally with SpringTrail stagger entrance. Scene 5 reuses the layout but shifts emphasis: left panel animates to opacity:0.5 + blur(4px) via spring, right panel spring-scales to 1.02. This creates a clear visual "winner".

**Scene 6 detail — Feature Demo:**
Show a simplified UI mockup. UI elements enter with `ScalePop` (`SPRING.bouncy`). **GSAP CursorClick** is still recommended here for realistic cursor path + click ripple (spring can't easily simulate cursor movement). Mix: spring entrances for UI elements, GSAP for cursor interaction.

**Scene 7 detail — Showcase:**
Grid of cards (3x3 or 4x2). **Spring version (default):** `GridStagger` with `SPRING.pop` — center-out pop-in, distance-based delay calculation. After 30% of scene, overlay text springs in and grid blurs behind it. **Remotion version:** Simple staggered opacity with `interpolate()`.

**Scene 8 detail — CTA:**
**Spring version (default):** `SpringOutro` — brand name pops in with `SPRING.bouncy`, tagline springs in with delay. CTA button uses `ScalePop`. **GSAP version:** Outro with DrawSVG logo reveal + CursorClick on button.

---

## 2. Typographic Promo (18-25s, 7 scenes)

**Narrative arc:** Statement → Break → Statement → Break → Statement → Break → Closing

Pure typography and color. No product UI or mockups. Each text scene delivers one key message with visual emphasis through highlight boxes.

| # | Scene | Duration | Purpose | Default Pattern (Spring) | GSAP Alternative | Content Slot |
|---|-------|----------|---------|-------------------------|-------------------|---|
| 1 | Opening | 2-3s | First powerful statement | WordTrail (SPRING.stiff) | TitleCard or TextHighlightBox | Opening quote or hook |
| 2 | Visual Break A | 1-2s | Visual breathing room | ScalePop + SpringEntrance | PerspectiveEntrance or full-screen image | Abstract shape, icon, or footage |
| 3 | Statement B | 2-3s | Second key message | WordTrail + spring highlight | TextHighlightBox (needs SplitText) | Message with highlighted keywords |
| 4 | Visual Break B | 1-2s | Contrast moment | SpringCardFlip | CardFlip3D or full-screen image | Visual reveal on flip |
| 5 | Statement C | 2-3s | Third key message | useSpringEnterExit text swap | RotateXTextSwap | Swap between contrasting ideas |
| 6 | Visual Break C | 1-2s | Final visual | ScalePop shape entrance | Full-screen image or shape | Transition to closing |
| 7 | Closing | 2-3s | Brand + tagline | SpringOutro | Outro (GSAP for DrawSVG logo) | Brand name + tagline |

**Note:** For Bold Typography preset, GSAP TextHighlightBox (Scene 3) is often preferred because it requires SplitText for word-level positioning of highlight boxes. Spring alternatives work well for all other scenes.

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

**Spring version (default):**

| Step | Timing | Animation | Spring Config |
|------|--------|-----------|--------------|
| 1. Cards pop in | 0-18f | `ScalePop` stagger 3 frames | `SPRING.pop` |
| 2. Bars extend | 12-27f | `scaleX: 0→1` via spring | `SPRING.snappy` |
| 3. Text fade in | 21-30f | opacity + translateY via spring | `SPRING.smooth` |
| 4. Hold | 30-120f | Static display | — |
| 5. Reverse exit | 120-150f | `useSpringEnterExit` reverse | `SPRING.stiff` |

**GSAP version (for complex overlays):**

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
