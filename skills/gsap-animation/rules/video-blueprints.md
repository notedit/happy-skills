---
name: video-blueprints
description: Reusable scene-by-scene blueprints for common motion graphics video types
metadata:
  tags: gsap, remotion, video, blueprint, saas, promo, typography, social-media
---

## Blueprint Selection Guide

| Video Type | Duration | Scenes | Best For |
|-----------|----------|--------|----------|
| SaaS Product Promo | 22-30s | 8 | Landing page hero, product launch, feature announcement |
| Typographic Promo | 18-25s | 7 | Brand manifesto, quote video, lyric-style |
| Social Media Overlay | 4-6s | 1 | Transparent overlays for compositing in editors |

---

## 1. SaaS Product Promo (22-30s, 8 scenes)

Narrative arc: **Hook -> Question -> Brand -> Benefit -> Comparison -> Demo -> Showcase -> CTA**

| Scene | Duration | Template / Pattern | Content |
|-------|----------|--------------------|---------|
| 1. Hook | 2-3s | TitleCard + PerspectiveEntrance | Bold statement, two elements enter from sides |
| 2. Question | 2-3s | CardFlip3D | Pain point on front, solution tease on back |
| 3. Brand Reveal | 2-3s | charCascade effect | Product name with character animation |
| 4. Core Benefit | 3-4s | SplitScreenComparison | Before/after or old-way/new-way |
| 5. Comparison | 3-4s | SplitScreenComparison (dimLeft) | Left dims, right pops -- winner is clear |
| 6. Feature Demo | 3-4s | CursorClick | Simulated UI interaction |
| 7. Showcase | 3-4s | Remotion native grid | Feature grid or screenshot montage |
| 8. CTA | 2-3s | Outro + CursorClick | Call to action with simulated button click |

**Scene transitions:** Use `circleReveal` or `wipeIn` between scenes. Overlap transitions with `-=0.3`.

---

## 2. Typographic Promo (18-25s, 7 scenes)

Alternating text-heavy scenes with full-screen visual breaks. No product UI -- pure typography and color.

| Scene | Duration | Template / Pattern | Content |
|-------|----------|--------------------|---------|
| 1. Opening | 2-3s | TitleCard | Single powerful word or phrase |
| 2. Statement A | 2-3s | TextHighlightBox | Key message with highlighted words |
| 3. Visual Break | 1-2s | PerspectiveEntrance | Abstract shape or icon |
| 4. Statement B | 2-3s | RotateXTextSwap | Swap between two contrasting ideas |
| 5. Visual Break | 1-2s | CardFlip3D | Reveal visual on flip |
| 6. Statement C | 2-3s | TextHighlightBox | Final key message |
| 7. Closing | 2-3s | Outro | Brand name + tagline |

**Typography rules:**
- Unified font size across all text scenes (72-96px)
- Line height: 0.8 for tight, impactful typography
- Max width: 70% of viewport for comfortable reading
- Center-aligned, vertically centered

---

## 3. Social Media Overlay (4-6s, transparent background)

Single-scene overlay rendered with alpha channel for compositing in video editors.

**Sequence:** Staggered card pop-in -> bar extend -> text fade-in -> hold (1-2s) -> reverse exit

| Step | Duration | Animation |
|------|----------|-----------|
| Cards enter | 0.4-0.6s | `from { scale: 0, opacity: 0 }` with stagger 0.1s, `back.out(2)` |
| Bars extend | 0.3-0.5s | `from { scaleX: 0, transformOrigin: 'left' }` |
| Text fade | 0.2-0.3s | `from { opacity: 0, y: 10 }` |
| Hold | 1-2s | Static |
| Reverse exit | 0.5-0.8s | Reverse the entrance sequence |

**Rendering:** Use ProRes 4444 or WebM VP9 for alpha channel support (see SKILL.md Rendering section).

---

## Scene-to-Template Mapping

Quick reference for which SKILL.md pattern to use for each scene type:

| Scene Need | Pattern / Template |
|-----------|-------------------|
| Bold opening statement | TitleCard |
| Character-by-character text | charCascade effect |
| Reveal hidden information | CardFlip3D |
| Side-by-side comparison | SplitScreenComparison |
| Emphasize specific words | TextHighlightBox |
| Swap between two messages | RotateXTextSwap |
| Two elements converge | PerspectiveEntrance |
| Simulate user interaction | CursorClick |
| Closing with brand | Outro |
| Scene transition | circleReveal / wipeIn effects |
