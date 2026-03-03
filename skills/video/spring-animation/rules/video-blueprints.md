---
name: video-blueprints
description: Scene-by-scene blueprints for motion graphics videos using spring physics
metadata:
  tags: spring, remotion, video, blueprint, motion-graphics
---

## Blueprint Selection Guide

| Video Type | Duration | Scenes | Spring Character |
|-----------|----------|--------|-----------------|
| Bouncy Product Promo | 20-28s | 7 | Energetic pops, playful staggers |
| Elegant Reveal | 18-25s | 6 | Smooth springs, heavy mass, no bounce |
| Playful Social | 8-15s | 4 | Wobbly, rubber, extreme overshoot |

---

## 1. Bouncy Product Promo (20-28s, 7 scenes)

Narrative: **Pop -> Problem -> Solution -> Features -> Proof -> Demo -> CTA**

| Scene | Duration | Spring Pattern | Preset | Content |
|-------|----------|---------------|--------|---------|
| 1. Pop Hook | 2-3s | ScalePop + CharacterTrail | `pop` | Product name pops in, tagline trails |
| 2. Problem | 2-3s | SpringEntrance (up) | `snappy` | Pain point text slides up |
| 3. Solution | 3-4s | SpringCardFlip | `heavy` | Card flips to reveal solution |
| 4. Features | 3-4s | GridStagger (center-out) | `pop` | Feature icons pop from center |
| 5. Social Proof | 2-3s | SpringTrail (left) | `bouncy` | Stats/logos trail in |
| 6. Demo | 3-4s | SpringCrossfade | `smooth` | Screenshot with spring zoom |
| 7. CTA | 2-3s | SpringOutro | `pop` | CTA button pops, tagline gentle |

**Transitions:** Use `SpringSlide` or `SpringCrossfade` between scenes.

---

## 2. Elegant Reveal (18-25s, 6 scenes)

No bounce, no overshoot. Smooth springs with high damping and heavy mass. Luxury/premium feel.

| Scene | Duration | Spring Pattern | Preset | Content |
|-------|----------|---------------|--------|---------|
| 1. Ambient Open | 3-4s | Background + SpringEntrance | `molasses` | Slow background reveal |
| 2. Brand Name | 3-4s | WordTrail | `heavy` | Words appear with weight |
| 3. Statement | 3-4s | CharacterTrail | `gentle` | Key message, char by char |
| 4. Visual | 2-3s | PerspectiveTilt | `heavy` | Product image tilts into view |
| 5. Detail | 3-4s | SpringChain | `smooth` -> `gentle` | Sequential info reveal |
| 6. Close | 2-3s | SpringOutro | `gentle` | Calm, dignified close |

**Spring override:** Set `overshootClamping: true` on all springs for this style.

---

## 3. Playful Social (8-15s, 4 scenes)

Maximum bounce, extreme overshoot. Short, punchy, shareable.

| Scene | Duration | Spring Pattern | Preset | Content |
|-------|----------|---------------|--------|---------|
| 1. Bang | 1-2s | ScalePop + CharacterTrail | `rubber` | Title explodes in |
| 2. Key Point | 2-3s | WordTrail | `wobbly` | Words wobble into place |
| 3. Visual Pop | 2-3s | GridStagger | `pop` | Icons/emojis pop from center |
| 4. CTA | 2-3s | SpringOutro | `pop` | Bouncy CTA with strong overshoot |

**Speed:** Use `staggerFrames: 2` for fast-paced energy.

---

## Scene-to-Pattern Mapping

| Scene Need | Spring Pattern | Recommended Preset |
|-----------|---------------|-------------------|
| Bold opening | ScalePop / CharacterTrail | `pop` / `rubber` |
| Text entrance | WordTrail / CharacterTrail | `bouncy` / `pop` |
| Sequential info | SpringChain | `snappy` -> `gentle` |
| Grid of items | GridStagger | `pop` |
| List of items | SpringTrail | `bouncy` |
| Reveal information | SpringCardFlip | `heavy` |
| Scene change | SpringSlide / SpringCrossfade | `snappy` / `smooth` |
| Number display | SpringCounter | `bouncy` |
| 3D perspective | PerspectiveTilt | `heavy` |
| CTA / closing | SpringOutro | `pop` |
| Background | SpringEntrance (smooth) | `smooth` / `molasses` |
| Name overlay | SpringLowerThird | `snappy` (in) / `stiff` (out) |

---

## Combining with GSAP Scenes

Spring and GSAP blueprints can be mixed in the same video via `video-producer` skill:

| Scene Type | Use Spring When | Use GSAP When |
|-----------|----------------|---------------|
| Title | Bouncy/organic entrance | Text splitting with mask reveal |
| Comparison | Bouncy panel entrance | SplitScreenComparison with dim effect |
| Logo | Scale pop | DrawSVG stroke + fill |
| Text swap | N/A | RotateXTextSwap (3D text rotation) |
| Click sim | N/A | CursorClick (cursor + ripple) |
| Feature grid | Pop stagger | N/A (spring is better here) |
| Counter | Spring overshoot counter | N/A (spring is better here) |
