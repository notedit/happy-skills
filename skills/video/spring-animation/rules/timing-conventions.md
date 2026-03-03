---
name: timing-conventions
description: Spring config presets, timing standards, and physics parameters for motion graphics
metadata:
  tags: spring, timing, physics, presets, conventions
---

## Spring Config Quick Reference

| Preset | damping | stiffness | mass | Overshoot | Feel |
|--------|---------|-----------|------|-----------|------|
| smooth | 200 | 100 | 1 | None | Butter-smooth |
| snappy | 20 | 200 | 1 | Tiny | Crisp, responsive |
| bouncy | 8 | 100 | 1 | Strong | Playful, energetic |
| heavy | 15 | 80 | 2 | Small | Weighty, dramatic |
| wobbly | 4 | 80 | 1 | Extreme | Elastic, cartoon |
| stiff | 15 | 300 | 1 | Tiny | Mechanical, precise |
| gentle | 20 | 40 | 1.5 | Minimal | Dreamy, organic |
| molasses | 25 | 30 | 3 | Almost none | Cinematic, suspense |
| pop | 6 | 150 | 1 | Strong | Punchy scale-in |
| rubber | 3 | 100 | 0.5 | Extreme | Exaggerated bounce |

## Parameter Tuning Guide

### Damping (1-200)

Controls how quickly oscillation dies out.

| Value | Behavior | Use When |
|-------|----------|----------|
| 1-5 | Extreme bounce, many oscillations | Cartoon, comedy, exaggerated |
| 5-10 | Strong bounce, noticeable overshoot | Playful, energetic, attention |
| 10-20 | Light bounce, settles quickly | Standard UI, moderate energy |
| 20-50 | Barely bounces, smooth deceleration | Professional, subtle |
| 50-200 | No visible bounce, pure deceleration | Background, ambient, smooth |

### Stiffness (1-200)

Controls snap speed (how fast spring reaches target).

| Value | Behavior | Use When |
|-------|----------|----------|
| 20-50 | Slow, drifty approach | Dreamy, ambient, slow reveal |
| 50-100 | Medium speed (default feel) | Standard animations |
| 100-200 | Fast, snappy arrival | UI interactions, quick responses |
| 200+ | Very fast, almost instant | Stiff motion, mechanical feel |

### Mass (0.1-5)

Controls inertia and weight feel.

| Value | Behavior | Use When |
|-------|----------|----------|
| 0.1-0.5 | Light, responsive, quick | Small elements, particles |
| 0.5-1 | Standard weight | Default for most animations |
| 1-2 | Heavy, sluggish start | Large objects, dramatic reveals |
| 2-5 | Very heavy, slow momentum | Cinematic, weighty, massive objects |

## Timing Standards for Video

| Element | Preset | Delay | Notes |
|---------|--------|-------|-------|
| **Title entrance** | `pop` or `bouncy` | 0 | First element on screen |
| **Subtitle** | `gentle` | 10-15 frames | After title settles |
| **Word stagger** | `pop` | 4-6 frames apart | Per word |
| **Char stagger** | `pop` | 2-3 frames apart | Per character |
| **Container entrance** | `heavy` | 0 | Background/card |
| **Icon/badge pop** | `pop` | After parent | Small element accent |
| **List items** | `bouncy` | 3-5 frames apart | Sequential reveal |
| **Grid items** | `pop` | Distance-based | Center-out pattern |
| **Counter** | `bouncy` | 0 | Overshoot adds energy |
| **Lower third (in)** | `snappy` | 0 | Clean, professional |
| **Lower third (out)** | `stiff` | Near end | Quick, clean exit |
| **Scene transition** | `snappy` or `smooth` | At switch point | Between scenes |
| **CTA button** | `pop` | After content | Draw attention |
| **Background reveal** | `smooth` | 0 | Subtle, no bounce |
| **Card flip** | `heavy` | After hold | Weighty 3D rotation |

## Emotional Tone Mapping

| Tone | Primary Preset | Stagger | Speed |
|------|---------------|---------|-------|
| **Urgent** | `stiff` | 2-3 frames | Fast, minimal hold |
| **Exciting** | `bouncy` / `pop` | 3-4 frames | Medium, bouncy |
| **Professional** | `smooth` / `snappy` | 5-6 frames | Measured, clean |
| **Warm** | `gentle` | 6-8 frames | Slow, organic |
| **Playful** | `wobbly` / `rubber` | 3-5 frames | Medium, exaggerated |
| **Dramatic** | `heavy` / `molasses` | 8-12 frames | Slow, weighty |
| **Rebellious** | `stiff` + `rubber` mix | Irregular | Abrupt, chaotic |

## Video Format Standards

| Format | Resolution | FPS | Typical Duration |
|--------|-----------|-----|-----------------|
| YouTube landscape | 1920x1080 | 30 | 5-60s |
| Instagram Story | 1080x1920 | 30 | 5-15s |
| Instagram Reel | 1080x1920 | 30 | 15-90s |
| TikTok | 1080x1920 | 30 | 15-60s |
| Twitter/X | 1280x720 | 30 | 5-140s |

## Duration Calculator

```
frames = seconds * fps

At 30fps:
- 3s = 90 frames
- 5s = 150 frames
- 7s = 210 frames
- 10s = 300 frames
- 15s = 450 frames
```

## Motion Principles

1. **Springs over easing** -- spring physics feels alive; cubic-bezier feels mechanical
2. **Consistent configs** -- pick 2-3 presets per video and reuse
3. **Overshoot = energy** -- low damping adds personality; high damping adds professionalism
4. **Stagger creates rhythm** -- 2-4 frame stagger for chars, 4-6 for words, 8-12 for scenes
5. **Exit faster than enter** -- `stiff` for exits, `bouncy` for entrances
6. **Mass for hierarchy** -- heavier mass on larger/more important elements
7. **One bouncy hero** -- pick one element per scene to have strong bounce, keep others smooth
