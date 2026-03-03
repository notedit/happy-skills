---
name: remotion-integration
description: Core patterns for integrating spring physics with Remotion's frame-based rendering
metadata:
  tags: spring, remotion, integration, determinism, frame-based
---

## Core Principle

Remotion's `spring()` function is a **pure function of frame number**. Given the same frame, fps, and config, it always returns the same value. This makes it inherently deterministic and compatible with Remotion's parallel rendering.

```
Remotion Frame -> spring() -> Value (0 to ~1.2)
frame = 0      -> spring({frame: 0, ...})   -> 0.0
frame = 15     -> spring({frame: 15, ...})   -> 0.87  (with bounce)
frame = 30     -> spring({frame: 30, ...})   -> 1.02  (overshoot)
frame = 45     -> spring({frame: 45, ...})   -> 0.99  (settling)
frame = 60     -> spring({frame: 60, ...})   -> 1.00  (settled)
```

## Why NOT @react-spring/web

`@react-spring/web` cannot be used with Remotion because:

1. **Time-based**: Uses `requestAnimationFrame` internally -- not frame-driven
2. **Stateful**: Spring state accumulates over time -- no "seek to frame N"
3. **Non-deterministic rendering**: Parallel Remotion tabs would have different spring states
4. **React state dependency**: Uses `useState` internally for animation values

Remotion's native `spring()` solves all of these by computing the spring value as a pure function.

## Determinism Rules

1. **Always use `spring()`** -- never time-based animation libraries
2. **No `requestAnimationFrame`** -- Remotion controls rendering time
3. **No `setTimeout` / `setInterval`** -- use frame-based delays
4. **No `Date.now()`** -- use `useCurrentFrame()`
5. **No React state for animation values** -- derive from `spring()` + `useCurrentFrame()`
6. **Pure function of frame** -- same frame always produces same visual

## spring() + interpolate() Pattern

`spring()` returns 0-1 (can overshoot). Use `interpolate()` to map to any range.

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const progress = spring({ frame, fps, config: { damping: 10 } });

// Map to translation
const translateX = interpolate(progress, [0, 1], [-300, 0]);

// Map to rotation
const rotation = interpolate(progress, [0, 1], [0, 360]);

// Map to color-friendly value
const opacity = interpolate(progress, [0, 1], [0, 1], { extrapolateRight: 'clamp' });
```

**Note:** When spring overshoots (damping < 15), `progress` can exceed 1.0. Use `extrapolateRight: 'clamp'` for properties that shouldn't exceed their target (like opacity). Leave unclamped for properties where overshoot looks good (like scale, translateY).

## Delay Pattern

Delays in spring are frame-based. Two equivalent approaches:

```tsx
// Approach 1: spring delay parameter
const value = spring({ frame, fps, delay: 15, config: { damping: 10 } });

// Approach 2: manual frame offset (equivalent)
const value = spring({ frame: frame - 15, fps, config: { damping: 10 } });
// spring() returns 0 for negative frame values
```

Both are deterministic. Use `delay` parameter for clarity.

## Duration Constraint

By default, spring settles naturally based on physics. Use `durationInFrames` to force a specific duration:

```tsx
// Natural duration (depends on config)
const natural = spring({ frame, fps, config: { damping: 8 } });
// might take 45+ frames to settle

// Constrained duration
const constrained = spring({ frame, fps, config: { damping: 8 }, durationInFrames: 30 });
// compressed to exactly 30 frames
```

Use `measureSpring()` to calculate natural duration for `<Sequence>` timing:

```tsx
import { measureSpring } from 'remotion';

const duration = measureSpring({ fps: 30, config: { damping: 10 } });
// Use for <Sequence durationInFrames={duration}>
```

## Enter + Exit Pattern

The canonical spring enter/exit pattern using subtraction:

```tsx
const { durationInFrames } = useVideoConfig();

const enter = spring({ frame, fps, config: { damping: 200 } });
const exit = spring({
  frame, fps,
  config: { damping: 200 },
  durationInFrames: 20,
  delay: durationInFrames - 20,
});

const scale = enter - exit;
// 0 -> 1 (enter) -> 1 (hold) -> 0 (exit)
```

## Stagger Pattern (Trail)

Create staggered animations by offsetting spring delays:

```tsx
const items = ['A', 'B', 'C', 'D'];
const STAGGER = 4; // frames between each item

items.map((item, i) => {
  const progress = spring({ frame, fps, delay: i * STAGGER, config: { damping: 10 } });
  return <div style={{ opacity: progress }}>{item}</div>;
});
```

## Chain Pattern (Sequence)

Use `measureSpring()` to chain springs sequentially:

```tsx
const step1Config = { damping: 10 };
const step1Duration = measureSpring({ fps, config: step1Config });

const step1 = spring({ frame, fps, config: step1Config });
const step2 = spring({ frame, fps, delay: step1Duration, config: { damping: 15 } });
```

## Combining with GSAP

Spring and GSAP can coexist in the same composition. Use spring for physics-driven motion, GSAP for text splitting and SVG operations:

```tsx
const MyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring: bouncy container entrance
  const containerScale = spring({ frame, fps, config: { damping: 8 } });

  // GSAP: text split animation (SplitText can't be done with spring)
  const textRef = useGSAPWithFonts((tl, container) => {
    const split = SplitText.create(container.querySelector('.text')!, {
      type: 'chars', mask: 'chars',
    });
    tl.from(split.chars, { y: '100%', stagger: 0.03, duration: 0.5 });
  });

  return (
    <div style={{ transform: `scale(${containerScale})` }}>
      <div ref={textRef}>
        <h1 className="text">Hello Spring</h1>
      </div>
    </div>
  );
};
```

## Performance Tips

1. **spring() is cheap** -- pure math, no DOM, no side effects
2. **Call as many as needed** -- 20+ springs per component is fine
3. **No memoization needed** -- spring() already returns cached results for same inputs
4. **Use `<Sequence>` for scene isolation** -- each sequence gets its own frame counter
5. **Prefer spring for simple motion** -- don't add GSAP dependency just for fade/slide
