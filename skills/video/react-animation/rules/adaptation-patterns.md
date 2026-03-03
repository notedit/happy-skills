---
name: adaptation-patterns
description: Universal patterns for converting ReactBits components to Remotion frame-based rendering
metadata:
  tags: remotion, adaptation, patterns, interpolate, useCurrentFrame
---

## Core Principle

All ReactBits animations must be converted from event/time-driven to **frame-driven** rendering. Remotion renders each frame independently -- animations must be deterministic functions of the frame number.

## Pattern 1: Replace IntersectionObserver / ScrollTrigger with Frame Trigger

Many ReactBits components trigger on scroll visibility. In Remotion, trigger at a specific frame.

```tsx
// ReactBits (original)
const [inView, setInView] = useState(false);
useEffect(() => {
  const observer = new IntersectionObserver(([entry]) => {
    setInView(entry.isIntersecting);
  });
  observer.observe(ref.current);
}, []);

// Remotion (adapted)
const frame = useCurrentFrame();
const triggerFrame = 15; // start at 0.5s @ 30fps
const inView = frame >= triggerFrame;
```

For GSAP ScrollTrigger with scrub (scroll-linked progress):

```tsx
// ReactBits: gsap.fromTo(el, from, to) with ScrollTrigger scrub: true
// Remotion:
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const progress = interpolate(frame, [startFrame, endFrame], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
// Apply properties using progress (0 to 1)
const opacity = interpolate(progress, [0, 1], [0, 1]);
const y = interpolate(progress, [0, 1], [100, 0]);
```

## Pattern 2: Replace setInterval / setTimeout with Frame Math

```tsx
// ReactBits: setInterval(callback, intervalMs)
// Remotion:
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const intervalFrames = Math.round((intervalMs / 1000) * fps);
const currentIndex = Math.floor(frame / intervalFrames) % totalItems;
```

For typewriter effects:
```tsx
const framesPerChar = Math.round((typingSpeed / 1000) * fps);
const charsVisible = Math.min(
  Math.floor(frame / framesPerChar),
  text.length
);
const displayText = text.slice(0, charsVisible);
```

## Pattern 3: Replace useAnimationFrame / requestAnimationFrame with useCurrentFrame

```tsx
// ReactBits (Framer Motion)
useAnimationFrame((time, delta) => {
  progress.current += delta * speed;
});

// Remotion
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const progress = (frame / fps) * speed;
```

For Canvas 2D components:
```tsx
// ReactBits: requestAnimationFrame loop
// Remotion: render once per frame
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

useEffect(() => {
  const ctx = canvasRef.current.getContext('2d');
  const time = frame / fps;
  drawFrame(ctx, time); // your draw function
}, [frame]);
```

## Pattern 4: Replace Mouse/Pointer Input with Scripted Cursor Path

For optional mouse-enhancement effects (ScrambledText, shader backgrounds with mouse toggle):

```tsx
const frame = useCurrentFrame();
const { fps, width, height } = useVideoConfig();
const t = frame / fps;

// Circular path
const cursorX = width / 2 + (width * 0.3) * Math.sin(t * 1.5);
const cursorY = height / 2 + (height * 0.2) * Math.cos(t * 1.2);

// Or keyframed path
const cursorX = interpolate(frame, [0, 30, 60, 90], [100, 500, 300, 700]);
const cursorY = interpolate(frame, [0, 30, 60, 90], [200, 100, 400, 200]);
```

## Pattern 5: WebGL Uniform Updates from Frame

For OGL/Three.js shader components:

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Time uniform (replaces performance.now() * 0.001 or clock.getElapsedTime())
uniforms.iTime.value = frame / fps;
// or for OGL: program.uniforms.uTime.value = frame / fps;

// Mouse uniform (fixed or animated)
uniforms.iMouse.value.set(0.5, 0.5); // center
// or animated:
uniforms.iMouse.value.set(
  0.5 + 0.3 * Math.sin(frame / fps),
  0.5 + 0.2 * Math.cos(frame / fps * 0.7)
);
```

## Pattern 6: Deterministic Randomness

Remotion may render frames out of order or multiple times. `Math.random()` produces non-deterministic results. Use a seeded PRNG:

```tsx
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

// Use frame number + element index as seed
const rand = seededRandom(frame * 1000 + charIndex);
```

For noise-based effects, use a deterministic noise function (simplex/perlin) with frame as input instead of Math.random().

## Pattern 7: Replace Framer Motion Primitives

```tsx
// useMotionValue + useTransform -> interpolate
const x = interpolate(frame, [0, durationInFrames], [0, 100]);

// useSpring -> spring()
import { spring } from 'remotion';
const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });

// AnimatePresence enter/exit -> Sequence + interpolate
<Sequence from={0} durationInFrames={30}>
  {/* entering content */}
</Sequence>
```

## Pattern 8: Replace GSAP Easings with Remotion Easing

| GSAP Easing | Remotion Equivalent |
|-------------|-------------------|
| `power1.out` | `Easing.out(Easing.quad)` |
| `power2.out` | `Easing.out(Easing.cubic)` |
| `power3.out` | `Easing.out(Easing.cubic)` |
| `power4.out` | `Easing.out(Easing.bezier(0.25, 0.46, 0.45, 0.94))` |
| `back.inOut(2)` | `Easing.inOut(Easing.back(2))` |
| `elastic.out(1, 0.3)` | `Easing.out(Easing.elastic(1))` |
| `expo.out` | `Easing.out(Easing.exp)` |

```tsx
import { Easing, interpolate } from 'remotion';

const value = interpolate(frame, [startFrame, endFrame], [0, 1], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});
```

## Pattern 9: Stagger Animation (Per-Character/Word)

Many ReactBits text animations use staggered reveals. In Remotion:

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const staggerFrames = Math.round((staggerMs / 1000) * fps);
const durationFrames = Math.round(duration * fps);

{characters.map((char, i) => {
  const charStart = startFrame + i * staggerFrames;
  const progress = interpolate(
    frame,
    [charStart, charStart + durationFrames],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  const opacity = progress;
  const y = interpolate(progress, [0, 1], [40, 0]);
  return (
    <span key={i} style={{ opacity, transform: `translateY(${y}px)` }}>
      {char}
    </span>
  );
})}
```

## Pattern 10: Disabling Browser-Only Features

Remove these in all ReactBits-to-Remotion adaptations:
- `IntersectionObserver` -- always visible
- `ResizeObserver` -- use `useVideoConfig()` for fixed dimensions
- `window.addEventListener('resize')` -- fixed dimensions
- `document.fonts.load()` -- use `@remotion/google-fonts` or `staticFile()`
- `prefers-reduced-motion` -- not applicable in video
- `window.devicePixelRatio` -- use fixed DPR or Remotion's config
- `:hover` / `:active` CSS states -- not applicable in video
- `navigator.userAgent` mobile detection -- not applicable
