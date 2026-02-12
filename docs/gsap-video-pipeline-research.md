# GSAP + Remotion Integration Research

> Research Date: 2026-02-12

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [GSAP Licensing Context](#gsap-licensing-context)
3. [Core Integration: GSAP Timeline + Remotion Frame Model](#core-integration-gsap-timeline--remotion-frame-model)
4. [Making GSAP Deterministic in Remotion](#making-gsap-deterministic-in-remotion)
5. [GSAP Plugin Compatibility in Remotion](#gsap-plugin-compatibility-in-remotion)
6. [Time-Based vs Frame-Based: Bridging the Gap](#time-based-vs-frame-based-bridging-the-gap)
7. [Rendering Pipeline: Remotion CLI Output](#rendering-pipeline-remotion-cli-output)
8. [Audio Sync via Remotion](#audio-sync-via-remotion)
9. [Performance Considerations](#performance-considerations)
10. [Relationship to Existing react-animation Skill](#relationship-to-existing-react-animation-skill)
11. [When to Use GSAP vs Remotion's Built-in interpolate()](#when-to-use-gsap-vs-remotions-built-in-interpolate)
12. [Architecture Recommendations](#architecture-recommendations)

---

## Executive Summary

GSAP integrates with Remotion through a **seek-based synchronization pattern**: GSAP timelines are created in paused state, then on every frame Remotion's `useCurrentFrame()` value is converted to seconds and used to `seek()` the GSAP timeline to the exact position. This gives Remotion full control over time progression while GSAP handles the animation logic.

This approach is **deterministic**, **frame-perfect**, and leverages the existing Remotion infrastructure already in the project's `react-animation` skill. The GSAP skill should complement the react-animation skill by providing capabilities that Remotion's built-in `interpolate()` cannot easily replicate: complex timeline orchestration, advanced easing (CustomEase, RoughEase, SlowMo), SVG morphing (MorphSVG), path animation (MotionPath), and text splitting (SplitText).

As of late 2024, GSAP is 100% free (acquired by Webflow), including all previously paid plugins.

---

## GSAP Licensing Context

Webflow acquired GSAP in late 2024 and made it **100% free** for all uses, including commercial. All previously paid Club plugins are now freely available:

- **SplitText** -- text splitting and animation (completely rewritten, 50% smaller, 14 new features)
- **MorphSVG** -- SVG path morphing
- **DrawSVG** -- SVG stroke animation
- **MotionPathPlugin** -- animate along SVG/custom paths
- **CustomEase** -- custom easing curves from SVG paths / Bezier
- **CustomBounce** -- physics-based bounce easing
- **CustomWiggle** -- oscillation easing
- **EasePack** -- SlowMo, RoughEase, ExpoScaleEase
- **ScrollTrigger** -- scroll-linked animations (limited use in video)
- **Flip** -- layout transition animations
- **Draggable** -- drag interactions (not applicable in video)

No licensing concerns for production use.

---

## Core Integration: GSAP Timeline + Remotion Frame Model

### The Fundamental Pattern

Remotion requires all animations to be driven by `useCurrentFrame()`. GSAP uses time-based timelines. The bridge is a custom hook that **seeks** GSAP timelines to the time position corresponding to the current Remotion frame.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';
import gsap from 'gsap';
import { useRef, useEffect } from 'react';

/**
 * Syncs a GSAP timeline with Remotion's frame-based rendering.
 *
 * The timeline is created once (paused), then seek()'d on every frame.
 * Remotion controls time; GSAP provides the animation logic.
 */
function useGSAPTimeline(
  timelineFactory: (tl: gsap.core.Timeline) => void,
  deps: React.DependencyList = []
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tlRef = useRef<gsap.core.Timeline | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Create timeline once (or when deps change)
  useEffect(() => {
    const tl = gsap.timeline({ paused: true });
    timelineFactory(tl);
    tlRef.current = tl;
    return () => {
      tl.kill();
      tlRef.current = null;
    };
  }, deps);

  // Seek timeline to current frame's time position
  useEffect(() => {
    if (tlRef.current) {
      const timeInSeconds = frame / fps;
      tlRef.current.seek(timeInSeconds);
    }
  }, [frame, fps]);

  return { tlRef, containerRef };
}
```

### Usage Example

```tsx
const GSAPScene: React.FC = () => {
  const { containerRef } = useGSAPTimeline((tl) => {
    tl.from('.title', { opacity: 0, y: 50, duration: 1, ease: 'power2.out' })
      .from('.subtitle', { opacity: 0, y: 30, duration: 0.8, ease: 'power2.out' }, '-=0.5')
      .to('.title', { scale: 1.1, duration: 0.5, ease: 'elastic.out(1, 0.3)' }, '+=0.3');
  });

  return (
    <AbsoluteFill ref={containerRef}>
      <h1 className="title">Main Title</h1>
      <p className="subtitle">Subtitle text</p>
    </AbsoluteFill>
  );
};
```

### How seek() Works Internally

GSAP's `seek(timeInSeconds)` jumps the playhead to the specified position without affecting the paused/reversed state. Key properties:

| Method | Description | Use in Remotion |
|--------|-------------|-----------------|
| `seek(time)` | Jump to time (seconds) or label | Primary method -- called every frame |
| `progress(0-1)` | Get/set progress excluding repeats | Alternative -- use when total duration is known |
| `totalProgress(0-1)` | Get/set progress including repeats | For looping timelines |
| `time(seconds)` | Get/set local playhead position | Same as seek but getter/setter style |
| `totalTime(seconds)` | Including repeats and repeatDelays | For complex repeat patterns |
| `pause()` | Pause the timeline | Called once at creation |
| `totalDuration()` | Total duration including repeats | Useful for calculating Remotion composition duration |

### Remotion Integration Status

Remotion's official third-party integration docs list GSAP (GreenSock) as a supported community integration. There is no official `@remotion/gsap` package. Official packages exist for: Lottie, GIFs, Skia, Rive, Three.js, Vidstack.

The integration requires the custom `useGSAPTimeline` hook described above. This is a lightweight abstraction (< 30 lines) with no complex dependencies.

---

## Making GSAP Deterministic in Remotion

Remotion may render frames **out of order** and **multiple times** (for seeking, preview scrubbing, parallel chunk rendering). GSAP animations must produce identical output for any given frame number regardless of rendering order.

### Rule 1: Always Use Paused + Seek (Never Play)

```tsx
// CORRECT: deterministic
const tl = gsap.timeline({ paused: true });
tl.to('.box', { x: 500, duration: 2 });
tl.seek(frame / fps); // same frame always produces same state

// WRONG: non-deterministic
const tl = gsap.timeline(); // auto-plays
tl.to('.box', { x: 500, duration: 2 });
// State depends on when this code runs relative to real time
```

### Rule 2: No Real-Time Dependencies

Remove or replace anything that depends on wall-clock time:

| Forbidden | Replacement |
|-----------|-------------|
| `gsap.ticker.add(fn)` | Seek-based rendering (frame / fps) |
| `Date.now()` in callbacks | `frame / fps` for time values |
| `Math.random()` | Seeded PRNG: `seededRandom(frame * 1000 + index)` |
| `setTimeout` / `setInterval` | Frame-based triggers: `if (frame === targetFrame)` |
| `requestAnimationFrame` | `useCurrentFrame()` drives rendering |
| Callback-based logic (`onComplete`, `onUpdate`) | Frame range checks or Remotion `<Sequence>` |

### Rule 3: Seeded Randomness

```tsx
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

// Use frame + element index as seed for deterministic "random" values
const jitter = seededRandom(frame * 1000 + charIndex) * 10;
```

### Rule 4: No Stateful Animations

GSAP animations that accumulate state across frames will break. Each `seek()` must produce a complete, self-contained state.

```tsx
// CORRECT: GSAP seek fully resolves position at any time
tl.to('.box', { x: 500, duration: 2 });
tl.seek(1.0); // box is at x=250 (halfway)
tl.seek(0.5); // box is at x=125 (quarter way) -- works correctly

// PROBLEMATIC: onUpdate callbacks that accumulate state
let counter = 0;
tl.to('.box', { x: 500, duration: 2, onUpdate: () => counter++ });
// counter value depends on how many times seek() was called
```

### Rule 5: Avoid GSAP Callbacks for Visual Logic

GSAP callbacks (`onStart`, `onComplete`, `onUpdate`, `onRepeat`) may not fire as expected when using `seek()` instead of `play()`. For visual state changes at specific times, use Remotion's `<Sequence>` or frame-based conditionals.

```tsx
// Instead of onComplete callback, use frame checks:
const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Show element after animation completes (at 2 seconds)
const showElement = frame >= 2 * fps;
```

---

## GSAP Plugin Compatibility in Remotion

### Fully Compatible (Timeline-Based)

These plugins animate properties on a timeline and work perfectly with the seek pattern:

| Plugin | What It Does | Remotion Notes |
|--------|-------------|----------------|
| **Core tweens** | Animate CSS, transforms, SVG attributes | Works perfectly |
| **MorphSVG** | Morph between SVG path shapes | Excellent for motion graphics |
| **DrawSVG** | Animate SVG stroke drawing | Great for reveal effects |
| **MotionPathPlugin** | Animate along SVG/custom paths | Complex motion trajectories |
| **SplitText** | Split text into chars/words/lines then animate | Powerful text animation |
| **CustomEase** | Custom easing from SVG path / Bezier curves | Superior to Remotion's Easing |
| **CustomBounce** | Physics-based bounce easing | Realistic bounce effects |
| **CustomWiggle** | Oscillation easing | Vibration/wiggle effects |
| **EasePack** (SlowMo, RoughEase, ExpoScaleEase) | Advanced easing functions | Unique easing curves |
| **Flip** | FLIP-based layout transitions | With careful setup |
| **TextPlugin** | Animate text content changes | Typewriter-like effects |
| **AttrPlugin** | Animate HTML/SVG attributes | SVG attribute animation |
| **CSSPlugin** | Animate CSS properties (included in core) | Primary animation target |

### Partially Compatible (Requires Adaptation)

| Plugin | Issue | Workaround |
|--------|-------|------------|
| **ScrollTrigger** | No scroll in video | Replace with frame-range progress (see adaptation pattern below) |
| **Observer** | No user interaction | Not applicable in video |

**ScrollTrigger Adaptation Pattern:**

```tsx
// Original ScrollTrigger: scrub through animation as user scrolls
gsap.to('.box', {
  x: 500,
  scrollTrigger: { trigger: '.box', scrub: true }
});

// Remotion equivalent: scrub through animation based on frame progress
const frame = useCurrentFrame();
const progress = interpolate(frame, [startFrame, endFrame], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
// Use progress to drive GSAP or use Remotion's interpolate directly
```

### Not Compatible (Interaction-Based)

| Plugin | Reason |
|--------|--------|
| **Draggable** | Requires mouse/touch interaction |
| **Inertia** | Requires real-time velocity tracking |
| **Observer** (gesture mode) | Requires user gestures |

---

## Time-Based vs Frame-Based: Bridging the Gap

### The Core Conversion

```
GSAP time (seconds) = Remotion frame / fps
```

| Remotion Concept | GSAP Equivalent | Conversion |
|-----------------|-----------------|------------|
| `frame` (integer) | `time` (seconds) | `time = frame / fps` |
| `durationInFrames` | `duration` (seconds) | `duration = durationInFrames / fps` |
| `useCurrentFrame()` | `tl.time()` | `tl.seek(frame / fps)` |
| `<Sequence from={30}>` | Position parameter `"+=1"` | `from / fps` seconds offset |
| `interpolate(frame, ...)` | `gsap.to(target, { ... })` | GSAP handles interpolation internally |
| `spring({ frame, fps })` | `ease: 'elastic.out(1, 0.3)'` | GSAP easing replaces Remotion spring |
| `Easing.out(Easing.cubic)` | `ease: 'power2.out'` | See easing mapping table |

### Calculating Composition Duration from GSAP Timeline

```tsx
// After creating the timeline, get its total duration for Remotion
const tl = gsap.timeline({ paused: true });
tl.to('.a', { x: 100, duration: 1 })
  .to('.b', { y: 200, duration: 2 });

const totalSeconds = tl.totalDuration(); // 3 seconds
const durationInFrames = Math.ceil(totalSeconds * fps); // e.g., 90 frames at 30fps
```

### Easing Mapping: GSAP to Remotion

| GSAP Easing | Remotion Equivalent |
|-------------|---------------------|
| `power1.out` | `Easing.out(Easing.quad)` |
| `power2.out` | `Easing.out(Easing.cubic)` |
| `power3.out` | `Easing.out(Easing.cubic)` (approximate) |
| `power4.out` | `Easing.out(Easing.bezier(0.25, 0.46, 0.45, 0.94))` |
| `back.inOut(2)` | `Easing.inOut(Easing.back(2))` |
| `elastic.out(1, 0.3)` | `Easing.out(Easing.elastic(1))` |
| `expo.out` | `Easing.out(Easing.exp)` |
| `circ.out` | `Easing.out(Easing.circle)` |
| `sine.inOut` | `Easing.inOut(Easing.sin)` |
| **CustomEase(svgPath)** | **No Remotion equivalent** |
| **RoughEase** | **No Remotion equivalent** |
| **SlowMo** | **No Remotion equivalent** |

The bottom three (CustomEase, RoughEase, SlowMo) are key reasons to use GSAP inside Remotion -- they have no built-in Remotion equivalent.

### Combining GSAP and Remotion Animation in One Composition

GSAP and Remotion's `interpolate()` can coexist in the same component. Use GSAP for complex orchestrated sequences and Remotion's `interpolate()` for simple one-off property animations:

```tsx
const MyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Simple fade via Remotion (no need for GSAP)
  const backgroundOpacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Complex text sequence via GSAP
  const { containerRef } = useGSAPTimeline((tl) => {
    tl.from('.char', {
      opacity: 0, y: 50, rotationX: -90,
      stagger: 0.05, duration: 0.8,
      ease: 'back.out(1.7)',
    })
    .to('.char', {
      color: '#ff6600',
      stagger: 0.03, duration: 0.4,
      ease: CustomEase.create('custom', 'M0,0 C0.5,0 0.5,1 1,1'),
    }, '-=0.3');
  });

  return (
    <AbsoluteFill style={{ opacity: backgroundOpacity }}>
      <div ref={containerRef}>
        <SplitTextComponent text="Hello World" className="char" />
      </div>
    </AbsoluteFill>
  );
};
```

---

## Rendering Pipeline: Remotion CLI Output

### Supported Output Formats

| Format | Codec | Container | Quality | Speed | Notes |
|--------|-------|-----------|---------|-------|-------|
| **MP4 (H.264)** | libx264 | .mp4 | Very Good | Very Fast | Default; best browser compat |
| **MP4 (H.265)** | libx265 | .mp4 | Excellent | Fast | Better compression; poor browser support |
| **WebM (VP8)** | libvpx | .webm | Good | Slow | Smaller files |
| **WebM (VP9)** | libvpx-vp9 | .webm | Excellent | Very Slow | Smallest files |
| **ProRes** | prores_ks | .mov | Lossless | Fast | Professional editing; large files |
| **GIF** | gif | .gif | Low | Fast | No audio; supports every-nth-frame |
| **Image Sequence** | png/jpeg | folder | Lossless/Good | Fast | For post-production |

### CLI Rendering Commands

```bash
# Default MP4 (H.264)
npx remotion render src/index.ts MyComposition --output out/video.mp4

# High quality with custom CRF
npx remotion render src/index.ts MyComposition --codec h264 --crf 15

# WebM for web delivery
npx remotion render src/index.ts MyComposition --codec vp9 --output out/video.webm

# ProRes for professional editing
npx remotion render src/index.ts MyComposition --codec prores --prores-profile 4444

# GIF (every 2nd frame for smaller file)
npx remotion render src/index.ts MyComposition --codec gif --every-nth-frame 2

# Image sequence
npx remotion render src/index.ts MyComposition --image-format png --sequence

# With scale factor (render at 2x then downscale)
npx remotion render src/index.ts MyComposition --scale 2

# Transparent video (WebM VP8/VP9 with alpha)
npx remotion render src/index.ts MyComposition --codec vp8 --pixel-format yuva420p
```

### Quality Settings (CRF)

CRF controls quality-size tradeoff. Lower = better quality, larger file. +6 CRF roughly halves file size.

| Codec | Range | Default | Recommended |
|-------|-------|---------|-------------|
| H.264 | 1-51 | 18 | 15-20 for motion graphics |
| H.265 | 0-51 | 23 | 18-23 |
| VP8 | 4-63 | 9 | 4-10 |
| VP9 | 0-63 | 28 | 20-30 |

### Programmatic Rendering API

```tsx
import { renderMedia, bundle } from '@remotion/bundler';

const bundled = await bundle({ entryPoint: './src/index.ts' });

await renderMedia({
  composition: { id: 'MyComp', durationInFrames: 150, fps: 30, width: 1920, height: 1080 },
  serveUrl: bundled,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  crf: 18,
});
```

---

## Audio Sync via Remotion

### Built-in Audio Support

Remotion provides native audio components that are frame-synchronized with the video:

```tsx
import { Audio, Sequence, staticFile } from 'remotion';

const MyComposition: React.FC = () => (
  <AbsoluteFill>
    {/* Background music */}
    <Audio src={staticFile('bgm.mp3')} volume={0.5} />

    {/* Sound effect at specific time */}
    <Sequence from={30} durationInFrames={60}>
      <Audio src={staticFile('whoosh.mp3')} volume={0.8} />
    </Sequence>

    {/* GSAP-animated visuals */}
    <GSAPScene />
  </AbsoluteFill>
);
```

### Audio Properties

| Property | Description |
|----------|-------------|
| `src` | Audio file URL or staticFile() |
| `volume` | Number (0-1) or callback `(frame) => number` for dynamic volume |
| `startFrom` | Start playback from this frame of the audio |
| `endAt` | End audio at this frame |
| `playbackRate` | Speed multiplier |
| `muted` | Boolean to mute |

### Dynamic Volume Synced with GSAP Animation

```tsx
// Fade audio in sync with GSAP visual fade
<Audio
  src={staticFile('music.mp3')}
  volume={(f) => interpolate(f, [0, 30], [0, 1], { extrapolateRight: 'clamp' })}
/>
```

### Audio Encoding

Remotion handles AAC audio chunk concatenation with sophisticated alignment:
- Each AAC packet contains exactly 1024 samples
- Audio duration is padded to align with packet boundaries
- 512-sample silence at file start is compensated with negative MP4 container offset
- Result: **seamless audio concatenation** even with parallel chunk rendering

Supported audio codecs: AAC (default for MP4), MP3, PCM-16 (default for ProRes), Opus (for WebM).

---

## Performance Considerations

### GSAP seek() Performance in Frame-by-Frame Rendering

Remotion renders each frame independently. For every frame, the `useGSAPTimeline` hook calls `tl.seek(time)`. Key performance factors:

**Timeline Complexity:**
- `seek()` must resolve all tweens at the given time
- Nested timelines with many children increase seek cost
- Recommended: keep timelines under ~100 tweens for smooth rendering

**DOM Operations:**
- GSAP modifies DOM properties on each seek (transforms, opacity, etc.)
- Heavy DOM manipulation (many elements, complex CSS) slows per-frame rendering
- SplitText splitting into hundreds of characters can be expensive

**Optimization Strategies:**

```tsx
// 1. Use React.memo for non-animated containers
const Background = React.memo(() => (
  <div style={{ background: '#000', position: 'absolute', inset: 0 }} />
));

// 2. Use Remotion's <Freeze> for static segments
import { Freeze } from 'remotion';

<Sequence from={90}>
  <Freeze frame={0}>
    {/* This stops re-rendering after the animation completes */}
    <GSAPAnimatedElement />
  </Freeze>
</Sequence>

// 3. Scope GSAP to only necessary elements
const { containerRef } = useGSAPTimeline((tl) => {
  // Use containerRef scope so GSAP only queries within this container
  tl.from(containerRef.current!.querySelectorAll('.item'), {
    opacity: 0, stagger: 0.1, duration: 0.5,
  });
});

// 4. Avoid GPU-heavy CSS properties in cloud rendering
// Prefer transforms over box-shadow, filter:blur(), etc.
```

### Rendering Concurrency

```bash
# Find optimal concurrency for your system
npx remotion benchmark

# Render with specific concurrency
npx remotion render src/index.ts MyComp --concurrency 4

# Use verbose logging to find slow frames
npx remotion render src/index.ts MyComp --log=verbose
```

### Performance Comparison: GSAP seek() vs Remotion interpolate()

| Aspect | GSAP seek() | Remotion interpolate() |
|--------|-------------|----------------------|
| Per-frame cost | Higher (DOM mutations + tween resolution) | Lower (pure math) |
| Memory | Timeline object + all tweens in memory | Minimal (stateless) |
| Parallelism | Each frame must create timeline + seek | Stateless -- naturally parallel |
| Complexity handling | Excellent for 10+ property orchestrations | Verbose for complex sequences |
| Rendering speed | ~1.5-3x slower per frame (estimated) | Baseline |

**Recommendation:** Use GSAP only when its capabilities are needed. For simple fades, slides, and single-property animations, Remotion's `interpolate()` is faster and simpler.

### GPU Considerations

GSAP commonly animates CSS properties that may be GPU-intensive:
- `filter: blur()` -- very slow without GPU
- `box-shadow` -- CPU-rendered in headless Chrome
- `clip-path` -- varies by complexity
- `transform: matrix3d()` -- generally fast
- WebGL shaders -- require GPU-enabled rendering

For cloud/Lambda rendering without GPU, prefer transform-based animations over filter-based ones.

---

## Relationship to Existing react-animation Skill

### Current react-animation Skill Architecture

The existing skill at `skills/react-animation/` provides:
- **35 curated ReactBits components** organized by aesthetic category (Elegant, Modern, Luxury, Retro, Energy, Abstract, Utility)
- **Adaptation patterns** (`rules/adaptation-patterns.md`) for converting interactive components to Remotion's frame-based model
- **Aesthetic guidelines** for style consistency (max 2 styles per video)
- Components use Remotion's `useCurrentFrame()`, `interpolate()`, `spring()`, and `Easing`

### How GSAP Skill Complements react-animation

| Capability | react-animation | GSAP Skill |
|------------|----------------|------------|
| **Component library** | 35 pre-built visual components | Custom animation code |
| **Animation authoring** | Remotion interpolate/spring | GSAP timeline API |
| **Visual effects** | Shader backgrounds, text effects | Timeline-orchestrated sequences |
| **Ease of use** | Pick components, compose | Write timeline code |
| **Text animation** | BlurText, GlitchText, ShinyText, etc. | SplitText + custom per-char animation |
| **SVG animation** | Basic CSS/interpolate | MorphSVG, DrawSVG, MotionPath |
| **Easing** | Remotion Easing (standard curves) | CustomEase, RoughEase, SlowMo |
| **Sequencing** | `<Sequence>` component | Timeline position parameters |
| **Background effects** | Aurora, Silk, Particles, Lightning, etc. | Not the focus |
| **Best for** | Visually rich backgrounds + text reveals | Complex choreographed motion sequences |

### Complementary Usage Pattern

```tsx
// Combine both skills: react-animation components + GSAP orchestration
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from 'remotion';
import { Aurora } from './components/Aurora'; // from react-animation skill
import { useGSAPTimeline } from './hooks/useGSAPTimeline'; // from GSAP skill

const CombinedScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // GSAP handles complex text choreography
  const { containerRef } = useGSAPTimeline((tl) => {
    tl.from('.word', {
      opacity: 0, y: 80, rotationX: -90,
      stagger: { each: 0.1, from: 'center' },
      duration: 1,
      ease: 'back.out(1.7)',
    })
    .to('.word', {
      color: '#ff6600',
      stagger: { each: 0.05, from: 'edges' },
      duration: 0.5,
      ease: CustomEase.create('custom', 'M0,0 C0.126,0.382 0.282,1.567 0.504,1 0.702,0.495 0.818,0.936 1,1'),
    }, '-=0.5');
  });

  return (
    <AbsoluteFill>
      {/* Background from react-animation skill */}
      <Aurora time={frame / fps} colorStops={['#3A29FF', '#FF94B4', '#FF3232']} />

      {/* GSAP-orchestrated text */}
      <div ref={containerRef} style={{ position: 'relative', zIndex: 1 }}>
        {'CREATIVE STUDIO'.split(' ').map((word, i) => (
          <span key={i} className="word" style={{ display: 'inline-block', marginRight: 20 }}>
            {word}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

### Shared Patterns

Both skills share these adaptation patterns (documented in `rules/adaptation-patterns.md`):
- Frame-based animation (useCurrentFrame)
- Seeded randomness (deterministic PRNG)
- Shader uniform updates from frame number
- Scripted cursor paths (replacing mouse interaction)
- Disabling browser-only features (IntersectionObserver, ResizeObserver, etc.)

The GSAP skill should reuse and reference these existing patterns rather than duplicating them.

---

## When to Use GSAP vs Remotion's Built-in interpolate()

### Use Remotion interpolate() When:

- Single-property animations (fade, slide, scale)
- Simple sequences (`<Sequence from={30}>`)
- Spring physics (`spring({ frame, fps, config })`)
- Standard easing curves (cubic, quad, elastic, back, etc.)
- Color interpolation
- Number-to-string interpolation
- The animation logic is straightforward

### Use GSAP When:

- **Complex timeline orchestration**: Multiple elements with overlapping, staggered timing and the position parameter (`"-=0.5"`, `"<0.3"`, `"myLabel+=1"`)
- **Advanced easing**: CustomEase from SVG paths, RoughEase for organic feel, SlowMo for cinematic speed ramps
- **SplitText**: Per-character/word/line animation with automatic splitting
- **MorphSVG**: Morphing between arbitrary SVG path shapes
- **DrawSVG**: SVG stroke drawing/erasing animation
- **MotionPath**: Animating elements along complex SVG paths
- **Stagger with advanced options**: `from: 'center'`, `from: 'edges'`, `grid`, `axis`, custom distribution
- **Relative/incremental values**: `"+=100"`, `"*=2"`, `">>"` for sequential placement
- **Labels and control**: Named positions in timeline for complex choreography
- **Keyframes**: Multi-step property animations in a single tween

### Decision Flowchart

```
Is it a single property animation?
  YES -> Use Remotion interpolate()
  NO  -> Does it need complex timing (overlapping, stagger, labels)?
           YES -> Use GSAP timeline
           NO  -> Does it need advanced easing (CustomEase, RoughEase)?
                    YES -> Use GSAP
                    NO  -> Does it need SVG morphing/drawing/path?
                             YES -> Use GSAP (MorphSVG/DrawSVG/MotionPath)
                             NO  -> Does it need text splitting?
                                      YES -> Use GSAP SplitText
                                      NO  -> Use Remotion interpolate()
```

---

## Architecture Recommendations

### Package Dependencies

```json
{
  "dependencies": {
    "gsap": "^3.13.0",
    "@gsap/react": "^2.1.0",
    "remotion": "^4.x",
    "@remotion/cli": "^4.x"
  }
}
```

Note: `@gsap/react` provides the `useGSAP` hook for cleanup, but in the Remotion context we use a custom `useGSAPTimeline` hook that handles frame synchronization. The `@gsap/react` package is still useful for its `gsap.context()` cleanup capabilities.

### Plugin Registration

```tsx
// Register all GSAP plugins once at app entry
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';
import { CustomEase } from 'gsap/CustomEase';
import { CustomBounce } from 'gsap/CustomBounce';
import { CustomWiggle } from 'gsap/CustomWiggle';

gsap.registerPlugin(
  SplitText,
  MorphSVGPlugin,
  DrawSVGPlugin,
  MotionPathPlugin,
  CustomEase,
  CustomBounce,
  CustomWiggle,
);
```

### File Structure Recommendation

```
skills/gsap-animation/
├── SKILL.md                    # Skill documentation
├── rules/
│   ├── gsap-remotion-patterns.md  # GSAP + Remotion integration patterns
│   └── gsap-easing-guide.md       # Easing reference and CustomEase patterns
├── hooks/
│   └── useGSAPTimeline.ts         # Core integration hook (reference impl)
└── examples/
    ├── text-animation.md          # SplitText + stagger examples
    ├── svg-morphing.md            # MorphSVG examples
    ├── path-animation.md          # MotionPath examples
    └── timeline-orchestration.md  # Complex timeline patterns
```

### Key Design Principles

1. **GSAP is the animation layer; Remotion is the rendering pipeline.** GSAP provides the animation API. Remotion provides frame-by-frame rendering, audio, video encoding, and output.

2. **Complement, don't replace.** The GSAP skill adds capabilities the react-animation skill lacks (timeline orchestration, advanced easing, SVG plugins). It does not replace ReactBits components for visual effects.

3. **Determinism is non-negotiable.** Every GSAP animation must produce identical output for any given frame number, regardless of rendering order.

4. **Seek, never play.** All timelines are created paused and driven by `seek()`. This is the fundamental integration contract.

5. **Prefer simplicity.** If Remotion's `interpolate()` can do it, use that. Reach for GSAP only when its unique capabilities are needed.
