---
name: gsap-animation
description: GSAP + Remotion integration for professional motion graphics video production. Timeline orchestration, text splitting, SVG morphing, advanced easing, and reusable effect presets.
metadata:
  tags: gsap, remotion, motion-graphics, animation, video, text-animation, svg, timeline, easing
---

## When to use

Use this skill when creating Remotion video compositions that need **GSAP's advanced animation capabilities** beyond Remotion's built-in `interpolate()` and `spring()`.

**Use GSAP when you need:**
- Complex timeline orchestration (nesting, labels, position parameters like `"-=0.5"`)
- Text splitting animation (SplitText: chars/words/lines with mask reveals)
- SVG shape morphing (MorphSVG), stroke drawing (DrawSVG), path-following (MotionPath)
- Advanced easing (CustomEase from SVG paths, RoughEase, SlowMo, CustomBounce, CustomWiggle)
- Stagger with grid, center/edges distribution
- Character scramble/decode effects (ScrambleText)
- Reusable named effects via `gsap.registerEffect()`

**Use Remotion native `interpolate()` when:**
- Simple single-property animations (fade, slide, scale) -- do NOT use GSAP for these
- Numeric counters/progress bars -- pure math, no timeline needed
- Standard easing curves
- Spring physics (`spring()`)

**GSAP Licensing:** All plugins are **100% free** since Webflow's 2024 acquisition (SplitText, MorphSVG, DrawSVG, etc.).

---

## Setup

```bash
# In a Remotion project
npm install gsap
```

```tsx
// src/gsap-setup.ts -- import once at entry point
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';
import { ScrambleTextPlugin } from 'gsap/ScrambleTextPlugin';
import { CustomEase } from 'gsap/CustomEase';
import { CustomBounce } from 'gsap/CustomBounce';
import { CustomWiggle } from 'gsap/CustomWiggle';

gsap.registerPlugin(
  SplitText, MorphSVGPlugin, DrawSVGPlugin, MotionPathPlugin,
  ScrambleTextPlugin, CustomEase, CustomBounce, CustomWiggle,
);

export { gsap };
```

---

## Core Hook: useGSAPTimeline

The bridge between GSAP and Remotion. Creates a paused timeline, seeks it to `frame / fps` every frame.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';
import gsap from 'gsap';
import { useRef, useEffect } from 'react';

function useGSAPTimeline(
  buildTimeline: (tl: gsap.core.Timeline, container: HTMLDivElement) => void
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ paused: true });
      buildTimeline(tl, containerRef.current!);
      tlRef.current = tl;
    }, containerRef);
    return () => { ctx.revert(); tlRef.current = null; };
  }, []);

  useEffect(() => {
    if (tlRef.current) tlRef.current.seek(frame / fps);
  }, [frame, fps]);

  return containerRef;
}
```

**For SplitText (needs font loading):**

```tsx
import { delayRender, continueRender } from 'remotion';

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

---

## 1. Text Animations

### SplitText Reveal (chars/words/lines)

```tsx
const TextReveal: React.FC<{ text: string }> = ({ text }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const split = SplitText.create(container.querySelector('.heading')!, {
      type: 'chars,words,lines', mask: 'lines',
    });
    tl.from(split.chars, {
      y: 100, opacity: 0, duration: 0.6, stagger: 0.03, ease: 'power2.out',
    });
  });

  return (
    <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef}>
        <h1 className="heading" style={{ fontSize: 80, fontWeight: 'bold' }}>{text}</h1>
      </div>
    </AbsoluteFill>
  );
};
```

**Patterns:**
| Pattern | SplitText Config | Animation |
|---------|-----------------|-----------|
| Line reveal | `type: "lines", mask: "lines"` | `from lines: { y: "100%" }` |
| Char cascade | `type: "chars"` | `from chars: { y: 50, opacity: 0, rotationX: -90 }` |
| Word scale | `type: "words"` | `from words: { scale: 0, opacity: 0 }` |
| Char + color | `type: "chars"` | `.from(chars, { y: 50 }).to(chars, { color: "#f00" })` |

### ScrambleText (decode effect)

> **Determinism warning:** ScrambleText uses internal random character selection. Use `--concurrency=1` when rendering to guarantee frame-perfect reproducibility across renders.

```tsx
const containerRef = useGSAPTimeline((tl, container) => {
  tl.to(container.querySelector('.text')!, {
    duration: 2,
    scrambleText: { text: 'DECODED', chars: '01', revealDelay: 0.5, speed: 0.3 },
  });
});
```

**Char sets:** `"upperCase"`, `"lowerCase"`, `"upperAndLowerCase"`, `"01"`, or custom string.

---

## 2. SVG Animations

### MorphSVG (shape morphing)

```tsx
const containerRef = useGSAPTimeline((tl, container) => {
  tl.to(container.querySelector('#path')!, {
    morphSVG: { shape: '#target-path', type: 'rotational', map: 'size' },
    duration: 1.5, ease: 'power2.inOut',
  });
});
```

| Option | Values |
|--------|--------|
| `type` | `"linear"` (default), `"rotational"` |
| `map` | `"size"`, `"position"`, `"complexity"` |
| `shapeIndex` | Integer for point alignment offset |

### DrawSVG (stroke animation)

```tsx
const containerRef = useGSAPTimeline((tl, container) => {
  const paths = container.querySelectorAll('.logo-path');
  tl.from(paths, { drawSVG: 0, duration: 1.5, stagger: 0.2, ease: 'power2.inOut' })
    .to(paths, { fill: '#ffffff', duration: 0.5 }, '-=0.3');
});
```

| Pattern | DrawSVG Value |
|---------|--------------|
| Draw from nothing | `0` |
| Draw from center | `"50% 50%"` |
| Show segment | `"20% 80%"` |
| Erase | `"100% 100%"` |

### MotionPath (path following)

```tsx
const containerRef = useGSAPTimeline((tl, container) => {
  tl.to(container.querySelector('.element')!, {
    motionPath: {
      path: container.querySelector('#svg-path') as SVGPathElement,
      align: container.querySelector('#svg-path') as SVGPathElement,
      alignOrigin: [0.5, 0.5],
      autoRotate: true,
    },
    duration: 3, ease: 'power1.inOut',
  });
});
```

---

## 3. Transitions

### Clip-Path Transitions

> **Performance note:** Complex clip-path animations (especially `polygon`) can slow down frame generation in Remotion's headless Chrome. If render times are high, consider replacing with opacity/transform-based alternatives or simplify to `circle`/`inset` shapes.

```tsx
const containerRef = useGSAPTimeline((tl, container) => {
  const scene = container.querySelector('.scene')!;

  // Circle reveal
  tl.fromTo(scene,
    { clipPath: 'circle(0% at 50% 50%)' },
    { clipPath: 'circle(75% at 50% 50%)', duration: 1, ease: 'power2.out' }
  );
});
```

| Transition | From | To |
|-----------|------|-----|
| Circle reveal | `circle(0% at 50% 50%)` | `circle(75% at 50% 50%)` |
| Wipe left | `polygon(0 0, 0 0, 0 100%, 0 100%)` | `polygon(0 0, 100% 0, 100% 100%, 0 100%)` |
| Iris | `polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)` | `polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)` |
| Blinds | `inset(0 0 100% 0)` | `inset(0 0 0% 0)` |

### Slide / Crossfade

```tsx
// Slide transition
tl.to(outgoing, { x: '-100%', duration: 0.6, ease: 'power2.inOut' })
  .fromTo(incoming, { x: '100%' }, { x: '0%', duration: 0.6, ease: 'power2.inOut' }, 0);

// Crossfade
tl.to(outgoing, { opacity: 0, duration: 1 })
  .fromTo(incoming, { opacity: 0 }, { opacity: 1, duration: 1 }, 0);
```

---

## 4. Templates

### Lower Third

```tsx
const LowerThird: React.FC<{ name: string; title: string; hold?: number }> = ({
  name, title, hold = 4,
}) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const bar = container.querySelector('.lt-bar')!;
    const nameEl = container.querySelector('.lt-name')!;
    const titleEl = container.querySelector('.lt-title')!;

    // In
    tl.fromTo(bar, { scaleX: 0, transformOrigin: 'left' }, { scaleX: 1, duration: 0.4, ease: 'power2.out' })
      .from(nameEl, { x: -30, opacity: 0, duration: 0.3 }, '-=0.1')
      .from(titleEl, { x: -20, opacity: 0, duration: 0.3 }, '-=0.1')
    // Hold
      .to({}, { duration: hold })
    // Out
      .to([bar, nameEl, titleEl], { x: -50, opacity: 0, duration: 0.3, stagger: 0.05, ease: 'power2.in' });
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef} style={{ position: 'absolute', bottom: 80, left: 60 }}>
        <div className="lt-bar" style={{ background: '#3b82f6', padding: '12px 24px', borderRadius: 4 }}>
          <div className="lt-name" style={{ fontSize: 28, fontWeight: 'bold', color: '#fff' }}>{name}</div>
          <div className="lt-title" style={{ fontSize: 18, color: 'rgba(255,255,255,0.8)' }}>{title}</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### Title Card

```tsx
const TitleCard: React.FC<{ mainTitle: string; subtitle?: string }> = ({ mainTitle, subtitle }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const bgShape = container.querySelector('.bg-shape')!;
    const titleEl = container.querySelector('.main-title')!;
    const divider = container.querySelector('.divider')!;

    tl.from(bgShape, { scale: 0, rotation: -45, duration: 0.8, ease: 'back.out(1.7)' });

    const split = SplitText.create(titleEl, { type: 'chars', mask: 'chars' });
    tl.from(split.chars, { y: '100%', duration: 0.5, stagger: 0.03, ease: 'power3.out' }, '-=0.3')
      .from('.subtitle', { y: 20, opacity: 0, duration: 0.6 }, '-=0.2')
      .from(divider, { scaleX: 0, duration: 0.4, ease: 'power2.out' }, '-=0.3');
  });

  return (
    <AbsoluteFill style={{ background: '#0f172a', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef} style={{ textAlign: 'center', color: '#fff' }}>
        <div className="bg-shape" style={{ position: 'absolute', width: 200, height: 200, borderRadius: '50%', background: 'rgba(59,130,246,0.2)', top: '30%', left: '45%' }} />
        <h1 className="main-title" style={{ fontSize: 80, fontWeight: 'bold', position: 'relative' }}>{mainTitle}</h1>
        <div className="divider" style={{ width: 80, height: 3, background: '#3b82f6', margin: '20px auto' }} />
        {subtitle && <p className="subtitle" style={{ fontSize: 32, opacity: 0.8 }}>{subtitle}</p>}
      </div>
    </AbsoluteFill>
  );
};
```

### Logo Reveal (DrawSVG)

```tsx
const LogoReveal: React.FC<{ svgContent: React.ReactNode; text?: string }> = ({ svgContent, text }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const paths = container.querySelectorAll('.logo-path');
    tl.from(paths, { drawSVG: 0, duration: 1.5, stagger: 0.1, ease: 'power2.inOut' })
      .to(paths, { fill: '#fff', duration: 0.5 }, '-=0.3');
    if (text) {
      tl.from(container.querySelector('.logo-text')!, { opacity: 0, x: -20, duration: 0.5 }, '-=0.2');
    }
  });

  return (
    <AbsoluteFill style={{ background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef} style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
        <svg viewBox="0 0 100 100" width={120} height={120}>{svgContent}</svg>
        {text && <span className="logo-text" style={{ fontSize: 48, color: '#fff', fontWeight: 'bold' }}>{text}</span>}
      </div>
    </AbsoluteFill>
  );
};
```

### Animated Counter

Uses Remotion's `interpolate()` for deterministic frame-by-frame calculation. No GSAP needed — counters are pure math.

```tsx
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

const AnimatedCounter: React.FC<{
  endValue: number; prefix?: string; suffix?: string; durationInSeconds?: number;
}> = ({ endValue, prefix = '', suffix = '', durationInSeconds = 2 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const value = interpolate(frame, [0, durationInSeconds * fps], [0, endValue], {
    extrapolateRight: 'clamp',
    easing: (t) => 1 - Math.pow(1 - t, 2), // power1.out equivalent
  });

  return (
    <div style={{ fontSize: 96, fontWeight: 'bold', fontVariantNumeric: 'tabular-nums' }}>
      {prefix}{Math.round(value).toLocaleString()}{suffix}
    </div>
  );
};
```

### Outro (closing scene)

```tsx
const Outro: React.FC<{ headline: string; tagline?: string; logoSvg?: React.ReactNode }> = ({
  headline, tagline, logoSvg,
}) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const headlineEl = container.querySelector('.outro-headline')!;
    const split = SplitText.create(headlineEl, { type: 'chars', mask: 'chars' });

    tl.from(split.chars, { y: '100%', duration: 0.5, stagger: 0.03, ease: 'power3.out' });
    if (tagline) {
      tl.from('.outro-tagline', { opacity: 0, y: 15, duration: 0.5, ease: 'power2.out' }, '-=0.2');
    }
    if (logoSvg) {
      const paths = container.querySelectorAll('.outro-logo path');
      tl.from(paths, { drawSVG: 0, duration: 1.2, stagger: 0.08, ease: 'power2.inOut' }, '-=0.3')
        .to(paths, { fill: '#fff', duration: 0.4 }, '-=0.2');
    }
  });

  return (
    <AbsoluteFill style={{ background: '#0f172a', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef} style={{ textAlign: 'center', color: '#fff' }}>
        <h1 className="outro-headline" style={{ fontSize: 72, fontWeight: 'bold' }}>{headline}</h1>
        {tagline && <p className="outro-tagline" style={{ fontSize: 28, opacity: 0.7, marginTop: 16 }}>{tagline}</p>}
        {logoSvg && <div className="outro-logo" style={{ marginTop: 40 }}>{logoSvg}</div>}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 5. Registered Effects

Pre-register effects for fluent timeline API. Import once at entry point.

```tsx
// lib/gsap-effects.ts
gsap.registerEffect({
  name: 'textReveal',
  effect: (targets, config) => {
    const split = SplitText.create(targets, { type: 'lines', mask: 'lines' });
    return gsap.from(split.lines, { y: '100%', duration: config.duration, stagger: config.stagger, ease: config.ease });
  },
  defaults: { duration: 0.6, stagger: 0.15, ease: 'power3.out' },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'charCascade',
  effect: (targets, config) => {
    const split = SplitText.create(targets, { type: 'chars' });
    return gsap.from(split.chars, { y: 50, opacity: 0, rotationX: -90, duration: config.duration, stagger: config.stagger, ease: config.ease });
  },
  defaults: { duration: 0.5, stagger: 0.02, ease: 'back.out(1.7)' },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'circleReveal',
  effect: (targets, config) => gsap.fromTo(targets,
    { clipPath: 'circle(0% at 50% 50%)' },
    { clipPath: 'circle(75% at 50% 50%)', duration: config.duration, ease: config.ease }),
  defaults: { duration: 1, ease: 'power2.out' },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'wipeIn',
  effect: (targets, config) => gsap.fromTo(targets,
    { clipPath: 'inset(0 100% 0 0)' },
    { clipPath: 'inset(0 0% 0 0)', duration: config.duration, ease: config.ease }),
  defaults: { duration: 0.8, ease: 'power2.inOut' },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'drawIn',
  effect: (targets, config) => gsap.from(targets, { drawSVG: 0, duration: config.duration, stagger: config.stagger, ease: config.ease }),
  defaults: { duration: 1.5, stagger: 0.1, ease: 'power2.inOut' },
  extendTimeline: true,
});

// Simple property animations (fade, slide, scale) should use Remotion's
// interpolate() directly — GSAP registered effects are reserved for
// operations that Remotion cannot do natively (SplitText, DrawSVG, etc.).
```

**Usage:**
```tsx
const containerRef = useGSAPTimeline((tl, container) => {
  tl.textReveal('.title')
    .charCascade('.subtitle', {}, '-=0.3')
    .circleReveal('.scene-2', {}, '+=0.5')
    .drawIn('.logo-path');
});
```

---

## 6. Easing Reference

| Motion Feel | GSAP Ease | Use Case |
|-------------|-----------|----------|
| Smooth deceleration | `power2.out` | Standard entrance |
| Strong deceleration | `power3.out` / `expo.out` | Dramatic entrance |
| Gentle acceleration | `power2.in` | Standard exit |
| Smooth both | `power1.inOut` | Scene transitions |
| Slight overshoot | `back.out(1.7)` | Attention, bounce-in |
| Elastic spring | `elastic.out(1, 0.5)` | Logo, playful |
| Bounce | `CustomBounce` | Impact, landing |
| Shake/vibrate | `CustomWiggle` | Attention, error |
| Organic/jagged | `RoughEase` | Tension, glitch |
| Custom curve | `CustomEase.create("id", "M0,0 C...")` | Brand-specific |
| Slow in middle | `slow(0.7, 0.7, false)` | Cinematic speed ramp |

**GSAP-only eases (no Remotion equivalent):** CustomEase, RoughEase, SlowMo, CustomBounce, CustomWiggle, ExpoScaleEase.

---

## 7. Combining with react-animation Skill

```tsx
const CombinedScene: React.FC = () => (
  <AbsoluteFill>
    {/* react-animation: visual atmosphere */}
    <Aurora colorStops={['#3A29FF', '#FF94B4']} />

    {/* gsap-animation: text + motion */}
    <GSAPTextReveal text="Beautiful Motion" />
    <GSAPLogoReveal svgContent={...} />

    {/* react-animation: film grain overlay */}
    <NoiseOverlay opacity={0.05} />
  </AbsoluteFill>
);
```

| Skill | Best For |
|-------|----------|
| **react-animation** | Visual backgrounds (Aurora, Silk, Particles), shader effects, WebGL |
| **gsap-animation** | Text animation, SVG motion, timeline orchestration, transitions, templates |

---

## 8. Composition Registration

```tsx
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="TitleCard" component={TitleCard}
      durationInFrames={120} fps={30} width={1920} height={1080}
      defaultProps={{ mainTitle: 'HELLO WORLD', subtitle: 'A GSAP Motion Story' }} />
    <Composition id="LowerThird" component={LowerThird}
      durationInFrames={210} fps={30} width={1920} height={1080}
      defaultProps={{ name: 'Jane Smith', title: 'Creative Director' }} />
    <Composition id="LogoReveal" component={LogoReveal}
      durationInFrames={90} fps={30} width={1920} height={1080}
      defaultProps={{ svgContent: <circle className="logo-path" cx={50} cy={50} r={40} fill="none" stroke="#fff" strokeWidth={2} />, text: 'BRAND' }} />
    <Composition id="Outro" component={Outro}
      durationInFrames={120} fps={30} width={1920} height={1080}
      defaultProps={{ headline: 'THANK YOU', tagline: 'See you next time' }} />
    {/* Social media variants */}
    <Composition id="IGStory-TitleCard" component={TitleCard}
      durationInFrames={150} fps={30} width={1080} height={1920}
      defaultProps={{ mainTitle: 'SWIPE UP' }} />
  </>
);
```

---

## 9. Rendering

```bash
# Default MP4
npx remotion render src/index.ts TitleCard --output out/title.mp4

# High quality
npx remotion render src/index.ts TitleCard --codec h264 --crf 15

# GIF
npx remotion render src/index.ts TitleCard --codec gif --every-nth-frame 2

# ProRes for editing
npx remotion render src/index.ts TitleCard --codec prores --prores-profile 4444

# With audio
# Use <Audio src={staticFile('bgm.mp3')} /> in composition
```
