---
name: timing-conventions
description: Standard timing, easing, and motion conventions for professional motion graphics
metadata:
  tags: gsap, timing, easing, motion-graphics, conventions
---

## Timing Standards

| Element | Duration | Ease | Notes |
|---------|----------|------|-------|
| **Text entrance (line)** | 0.5-0.8s | `power2.out` / `power3.out` | |
| **Text entrance (char stagger)** | 0.02-0.05s each | - | Gap between characters |
| **Text entrance (word stagger)** | 0.08-0.15s each | - | Gap between words |
| **Text entrance (line stagger)** | 0.1-0.2s each | - | Gap between lines |
| **Text exit** | 0.3-0.5s | `power2.in` | Faster than entrance |
| **Scene transition** | 0.5-1.0s | `power2.inOut` | |
| **Logo reveal (DrawSVG)** | 1.5-2.5s | `power2.inOut` | Slow, deliberate |
| **Shape morph** | 1.0-2.0s | `power2.inOut` | Smooth, cinematic |
| **Lower third (total)** | 4-6s | - | Entrance + hold + exit |
| **Hold for readable text** | 2-4s | - | ~250ms per word |
| **Counter animation** | 1.5-3.0s | `power1.out` | |
| **Dramatic entrance** | 0.5-1.0s | `expo.out` / `back.out(1.7)` | |
| **Attention pulse** | 0.3-0.5s | `sine.inOut` | repeat, yoyo |
| **Particle burst** | 1.0-2.0s | - | With gravity |
| **Bar chart grow** | 0.6-1.0s | `power2.out` | With stagger 0.1s |
| **3D card flip** | 1.0-1.5s | `power2.inOut` | perspective: 800 |
| **Perspective entrance** | 0.6-1.0s | `power3.out` | rotateY ±60deg |
| **RotateX text swap (out)** | 0.4-0.6s | `power2.in` | rotateX: 90, origin bottom |
| **RotateX text swap (in)** | 0.5-0.7s | `power2.out` | rotateX: -90, origin top |
| **Text highlight box** | 0.25-0.4s | `power2.out` | scaleX: 0→1 per word |
| **Highlight stagger** | 0.2-0.4s | - | Gap between highlight boxes |
| **Cursor travel** | 0.6-1.0s | `power2.inOut` | Off-screen to target |
| **Cursor click** | 0.2-0.3s | `power2.out` | Scale down 0.95 + release |
| **Cursor ripple** | 0.5-0.7s | `power2.out` | Expanding circle |
| **Split screen entrance** | 0.5-0.7s | `power2.out` | Per-panel stagger |
| **Panel dim/blur** | 0.4-0.6s | `power2.inOut` | opacity:0.5 + blur(4px) |

## Easing Reference

### Standard Eases

| Motion Feel | GSAP Ease | When to Use |
|-------------|-----------|-------------|
| Smooth deceleration | `power2.out` | Default entrance |
| Strong deceleration | `power3.out` | Dramatic entrance |
| Very strong decel | `expo.out` | High impact entrance |
| Gentle acceleration | `power2.in` | Default exit |
| Smooth symmetric | `power1.inOut` | Scene transitions |
| Slight overshoot | `back.out(1.7)` | Playful bounce-in |
| Strong overshoot | `back.out(2.5)` | Cartoon/exaggerated |
| Elastic spring | `elastic.out(1, 0.5)` | Logo, playful elements |
| Organic sine | `sine.inOut` | Breathing, pulsing |
| Linear | `none` | Typewriter, constant speed |

### Special Eases (GSAP-only, no Remotion equivalent)

| Ease | Effect | Use Case |
|------|--------|----------|
| `CustomEase.create("id", "M0,0 C...")` | Arbitrary SVG curve | Brand-specific motion |
| `CustomBounce.create("id", { strength, squash })` | Physical bounce | Impact, landing |
| `CustomWiggle.create("id", { wiggles, type })` | Oscillation | Shake, vibration |
| `rough({ strength, points, clamp })` | Jagged/organic | Tension, glitch, hand-drawn |
| `slow(slowRatio, endRatio, linear)` | Speed ramp | Cinematic slow-motion |
| `expoScale(start, end, ease)` | Exponential scale | Camera zoom feel |

### Position Parameters (Timeline Orchestration)

| Syntax | Meaning | Example |
|--------|---------|---------|
| `3` | At absolute 3s | `.to(el, { x: 100 }, 3)` |
| `"+=1"` | 1s after previous ends | `.to(el, { x: 100 }, "+=1")` |
| `"-=0.5"` | 0.5s before previous ends (overlap) | `.to(el, { x: 100 }, "-=0.5")` |
| `"<"` | At start of previous animation | `.to(el, { x: 100 }, "<")` |
| `"<0.3"` | 0.3s after start of previous | `.to(el, { x: 100 }, "<0.3")` |
| `">-0.2"` | 0.2s before end of previous | `.to(el, { x: 100 }, ">-0.2")` |
| `"myLabel"` | At named label | `.to(el, { x: 100 }, "myLabel")` |
| `"myLabel+=1"` | 1s after named label | `.to(el, { x: 100 }, "myLabel+=1")` |

### Stagger Options

| Config | Effect |
|--------|--------|
| `stagger: 0.1` | 0.1s between each element |
| `stagger: { each: 0.1, from: "center" }` | Radiate from center |
| `stagger: { each: 0.1, from: "edges" }` | Start from both edges |
| `stagger: { each: 0.1, from: "end" }` | Reverse order |
| `stagger: { each: 0.1, grid: [4, 6], axis: "y" }` | Grid pattern, Y axis |
| `stagger: (i) => seededRandom(i * 7919) * 0.5` | Deterministic "random" |

## Video Format Conventions

| Format | Resolution | FPS | Duration | Use Case |
|--------|-----------|-----|----------|----------|
| YouTube landscape | 1920x1080 | 30 | 5-60s | Standard web video |
| YouTube landscape (HQ) | 3840x2160 | 60 | 5-60s | 4K presentation |
| Instagram Story | 1080x1920 | 30 | 5-15s | Vertical story format |
| Instagram Reel | 1080x1920 | 30 | 15-90s | Vertical reel |
| TikTok | 1080x1920 | 30 | 15-60s | Vertical short |
| Twitter/X | 1280x720 | 30 | 5-140s | Horizontal short |
| LinkedIn | 1920x1080 | 30 | 10-30s | Professional content |

## Composition Duration Calculator

```
frames = seconds * fps

Examples (at 30fps):
- 3 second title card  = 90 frames
- 5 second lower third = 150 frames
- 7 second full scene  = 210 frames
- 15 second IG story   = 450 frames
```

## Motion Principles

1. **Entrances are slower than exits** -- 0.6s in, 0.3s out
2. **Overlap animations** -- use `"-=0.3"` to avoid sequential pauses
3. **Stagger creates rhythm** -- 0.03s for chars, 0.1s for words, 0.15s for lines
4. **Hold for readability** -- minimum 2s for any text that should be read
5. **Consistency within a video** -- pick one entrance ease and reuse
6. **Backgrounds stay subtle** -- slow, continuous movement behind animated text
7. **Film grain adds quality** -- Noise overlay at 0.03-0.08 opacity
8. **Max 2 style categories** -- don't mix elegant + retro, or luxury + glitch
