---
name: spring-presets
description: Predefined spring configurations and custom preset creation guide
metadata:
  tags: spring, presets, physics, config, customization
---

## Built-in Presets

Import from `spring-presets.ts`:

```tsx
import { SPRING } from './spring-presets';

spring({ frame, fps, config: SPRING.bouncy });
```

### Preset Definitions

```tsx
export const SPRING = {
  smooth:   { damping: 200 },
  snappy:   { damping: 20, stiffness: 200 },
  bouncy:   { damping: 8 },
  heavy:    { damping: 15, stiffness: 80, mass: 2 },
  wobbly:   { damping: 4, stiffness: 80 },
  stiff:    { damping: 15, stiffness: 300 },
  gentle:   { damping: 20, stiffness: 40, mass: 1.5 },
  molasses: { damping: 25, stiffness: 30, mass: 3 },
  pop:      { damping: 6, stiffness: 150 },
  rubber:   { damping: 3, stiffness: 100, mass: 0.5 },
} as const;
```

## Approximate Duration (at 30fps)

Use `measureSpring()` for exact values. These are approximations:

| Preset | ~Frames | ~Seconds |
|--------|---------|----------|
| smooth | 23 | 0.77s |
| snappy | 18 | 0.60s |
| bouncy | 55 | 1.83s |
| heavy | 65 | 2.17s |
| wobbly | 85 | 2.83s |
| stiff | 12 | 0.40s |
| gentle | 50 | 1.67s |
| molasses | 80 | 2.67s |
| pop | 60 | 2.00s |
| rubber | 100 | 3.33s |

## Custom Presets for Specific Styles

### Brand-Specific Presets

```tsx
// Tech startup -- fast, precise, minimal bounce
const TECH = {
  primary: { damping: 25, stiffness: 180 },
  secondary: { damping: 35, stiffness: 120 },
  background: { damping: 200, stiffness: 50 },
};

// Luxury brand -- slow, weighty, no bounce
const LUXURY = {
  primary: { damping: 40, stiffness: 40, mass: 2 },
  secondary: { damping: 50, stiffness: 30, mass: 1.5 },
  background: { damping: 200, stiffness: 20, mass: 3 },
};

// Kids/playful -- bouncy, energetic
const PLAYFUL = {
  primary: { damping: 5, stiffness: 120 },
  secondary: { damping: 8, stiffness: 100 },
  background: { damping: 15, stiffness: 60 },
};

// Editorial/news -- crisp, professional
const EDITORIAL = {
  primary: { damping: 30, stiffness: 200 },
  secondary: { damping: 40, stiffness: 150 },
  background: { damping: 200, stiffness: 80 },
};
```

### Animation-Role Presets

```tsx
// Per-role configs (use within any brand style)
const ROLES = {
  // First element to appear -- sets the energy
  hero: { damping: 8, stiffness: 100 },
  // Supporting text -- slightly calmer
  support: { damping: 15, stiffness: 120 },
  // Background/ambient -- never bounces
  ambient: { damping: 200, stiffness: 40 },
  // Exit animation -- fast, clean
  exit: { damping: 20, stiffness: 200 },
  // Attention grabber -- strong overshoot
  attention: { damping: 4, stiffness: 150 },
};
```

## Creating Custom Configs

### From Feel Description

| "I want it to feel..." | Start With | Then Adjust |
|------------------------|------------|-------------|
| Snappy but with a tiny bounce | `{ damping: 18, stiffness: 200 }` | Lower damping for more bounce |
| Heavy and dramatic | `{ damping: 15, stiffness: 60, mass: 2.5 }` | Increase mass for more weight |
| Elastic like a rubber band | `{ damping: 3, stiffness: 100, mass: 0.5 }` | Lower mass for faster oscillation |
| Smooth like butter | `{ damping: 200, stiffness: 80 }` | Increase damping to remove all bounce |
| Quick pop | `{ damping: 8, stiffness: 200 }` | Higher stiffness for faster arrival |

### Iteration Process

1. Start with the closest preset
2. Adjust ONE parameter at a time
3. Use Remotion Studio preview to check feel
4. Use `measureSpring()` to verify duration fits your scene

```tsx
// Test in Remotion Studio:
const testSpring = spring({
  frame,
  fps,
  config: { damping: 12, stiffness: 120, mass: 1.2 },
});
// Watch the preview, adjust until it feels right
```

## Clamped vs Unclamped

By default, springs can overshoot (value > 1.0). Use `overshootClamping` for properties that should never exceed target:

```tsx
// Unclamped (default) -- good for scale, translateY
const scale = spring({ frame, fps, config: SPRING.bouncy });
// Can be 1.15 at peak overshoot

// Clamped -- good for opacity, progress bars
const opacity = spring({
  frame, fps,
  config: { ...SPRING.bouncy, overshootClamping: true },
});
// Never exceeds 1.0
```

**Rule of thumb:**
- **Clamp:** opacity, clip-path progress, color interpolation input
- **Don't clamp:** scale, translateX/Y, rotation, width/height
