---
name: remotion-integration
description: Core patterns for integrating GSAP timelines with Remotion's frame-based rendering
metadata:
  tags: gsap, remotion, integration, useGSAPTimeline, determinism, frame-based
---

## Core Principle

GSAP timelines are created **paused** and **seeked** to `frame / fps` on every frame. Remotion controls time; GSAP provides animation logic. This produces deterministic, frame-perfect video output.

```
Remotion Frame -> Time Conversion -> GSAP Timeline Seek
frame = 0      -> tl.seek(0)       -> start state
frame = 15     -> tl.seek(0.5)     -> 0.5s state (@ 30fps)
frame = 30     -> tl.seek(1.0)     -> 1.0s state
```

## useGSAPTimeline Hook

```tsx
function useGSAPTimeline(
  buildTimeline: (tl: gsap.core.Timeline, container: HTMLDivElement) => void
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  // Build timeline once (paused)
  useEffect(() => {
    if (!containerRef.current) return;
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ paused: true });
      buildTimeline(tl, containerRef.current!);
      tlRef.current = tl;
    }, containerRef);
    return () => { ctx.revert(); tlRef.current = null; };
  }, []);

  // Seek to current frame
  useEffect(() => {
    if (tlRef.current) tlRef.current.seek(frame / fps);
  }, [frame, fps]);

  return containerRef;
}
```

## useGSAPWithFonts Hook (for SplitText)

SplitText measures text dimensions, so fonts must be loaded first. Use `delayRender()` to block rendering until ready.

```tsx
function useGSAPWithFonts(
  buildTimeline: (tl: gsap.core.Timeline, container: HTMLDivElement) => void
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);
  const [handle] = useState(() => delayRender());

  useEffect(() => {
    document.fonts.ready.then(() => {
      if (!containerRef.current) return;
      const ctx = gsap.context(() => {
        const tl = gsap.timeline({ paused: true });
        buildTimeline(tl, containerRef.current!);
        tlRef.current = tl;
      }, containerRef);
      continueRender(handle);
      return () => { ctx.revert(); };
    });
  }, []);

  useEffect(() => {
    if (tlRef.current) tlRef.current.seek(frame / fps);
  }, [frame, fps]);

  return containerRef;
}
```

## Determinism Rules

1. **Always paused + seek** -- never `tl.play()`, never `tl.resume()`
2. **No real-time deps** -- no `Date.now()`, `setTimeout`, `requestAnimationFrame`, `gsap.ticker`
3. **Seeded randomness** -- no `Math.random()` or `gsap.utils.random()`; use seeded PRNG
4. **No stateful callbacks** -- avoid `onUpdate` that accumulates state
5. **No interactive plugins** -- no Draggable, Observer, Inertia, ScrollTrigger
6. **No live DOM measurement** -- pre-calculate in build phase, not per-frame
7. **Pure function of frame** -- same frame number always produces same visual

```tsx
// Seeded random for deterministic "random" values
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

// Deterministic stagger (instead of from: "random")
tl.from(items, {
  y: 100, opacity: 0,
  stagger: (index) => seededRandom(index * 7919) * 0.5,
});
```

## Timeline Duration to Remotion Frames

```tsx
// Calculate Composition durationInFrames from GSAP timeline
const tl = gsap.timeline({ paused: true });
// ... build timeline ...
const totalSeconds = tl.totalDuration();
const durationInFrames = Math.ceil(totalSeconds * fps);
```

## Performance Tips

1. **Build once, seek per frame** -- timeline in `useEffect([], [])`, seek in `useEffect([frame])`
2. **Use `gsap.context()`** -- scopes animations to container, enables clean revert
3. **Use `React.memo`** for static containers around animated elements
4. **Use `<Freeze>`** for elements after their animation completes
5. **Keep timelines under ~100 tweens** -- `seek()` resolves all tweens at position
6. **Prefer transforms over filters** -- `filter: blur()` is slow without GPU
7. **SplitText: split once** in build phase, not per-frame

## Combining GSAP + Remotion interpolate()

Use GSAP for complex sequences, Remotion `interpolate()` for simple properties:

```tsx
const MyScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Simple fade via Remotion native (no GSAP needed)
  const bgOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  // Complex text sequence via GSAP
  const containerRef = useGSAPTimeline((tl, container) => {
    tl.from(container.querySelectorAll('.char'), {
      opacity: 0, y: 50, rotationX: -90,
      stagger: 0.05, duration: 0.8, ease: 'back.out(1.7)',
    });
  });

  return (
    <AbsoluteFill style={{ opacity: bgOpacity }}>
      <div ref={containerRef}>...</div>
    </AbsoluteFill>
  );
};
```

## Flickering Prevention (Parallel Rendering)

Remotion renders frames in multiple browser tabs in parallel. Each tab:
- Creates its own component instance
- Builds its own GSAP timeline
- Seeks independently

This works correctly because:
- Timeline construction is deterministic (same props = same timeline)
- `seek()` is stateless (same time = same output)
- No cross-frame state dependency

Avoid:
- `useState` for animation values (derive from `useCurrentFrame()`)
- Global mutable state
- GSAP's ticker or global timeline

## Audio Sync

Use Remotion's `<Audio>` + `<Sequence>` for frame-synced audio:

```tsx
<AbsoluteFill>
  <Audio src={staticFile('bgm.mp3')} volume={0.5} />
  <Sequence from={30} durationInFrames={60}>
    <Audio src={staticFile('whoosh.mp3')} volume={0.8} />
  </Sequence>
  <GSAPAnimatedScene />
</AbsoluteFill>
```
