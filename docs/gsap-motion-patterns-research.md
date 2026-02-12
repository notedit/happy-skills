# GSAP Motion Graphics Patterns Research

> Reference catalog for building a GSAP-based motion graphics skill for video production.
> All GSAP plugins are now **100% free** (including former Club GreenSock plugins) since Webflow's acquisition in 2024.
> **Rendering pipeline: GSAP + Remotion** -- all patterns shown as React components compatible with Remotion's frame-based rendering.

---

## Table of Contents

1. [GSAP + Remotion Integration](#1-gsap--remotion-integration)
2. [Core Animation Patterns](#2-core-animation-patterns)
3. [Text Animation Patterns](#3-text-animation-patterns)
4. [SVG/Shape Animation Patterns](#4-svgshape-animation-patterns)
5. [Transition Effects](#5-transition-effects)
6. [Motion Graphics Templates (Remotion Compositions)](#6-motion-graphics-templates-remotion-compositions)
7. [Advanced Techniques](#7-advanced-techniques)
8. [GSAP Plugins Reference](#8-gsap-plugins-reference)
9. [Utility Functions](#9-utility-functions)
10. [Reusable Effects System](#10-reusable-effects-system)
11. [GSAP vs After Effects](#11-gsap-vs-after-effects)
12. [Design Implications for Skill](#12-design-implications-for-skill)

---

## 1. GSAP + Remotion Integration

### 1.1 Core Integration Pattern: useGSAP + Remotion

Remotion renders each frame independently. GSAP timelines must be **paused** and **seeked** to the correct time on every frame. The pattern follows the same approach Remotion uses for Anime.js integration.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { useRef, useEffect, useState } from 'react';
import gsap from 'gsap';

/**
 * Core hook: syncs a GSAP timeline with Remotion's frame system.
 *
 * - Creates a paused timeline (autoplay disabled)
 * - On every frame, seeks the timeline to the correct time position
 * - Returns the timeline ref so the component can add animations
 * - Deterministic: same frame always produces same visual output
 */
function useGSAPTimeline(
  buildTimeline: (tl: gsap.core.Timeline, container: HTMLDivElement) => void
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  // Build timeline once on mount (paused)
  useEffect(() => {
    if (!containerRef.current) return;
    const tl = gsap.timeline({ paused: true });
    buildTimeline(tl, containerRef.current);
    tlRef.current = tl;
    return () => {
      tl.kill();
    };
  }, []);

  // Seek timeline to current frame's time position
  useEffect(() => {
    if (!tlRef.current) return;
    const timeInSeconds = frame / fps;
    tlRef.current.seek(timeInSeconds);
  }, [frame, fps]);

  return containerRef;
}
```

### 1.2 How useCurrentFrame Maps to GSAP Timeline

```
Remotion Frame System          GSAP Timeline
==================          ==============
frame = 0                  -> tl.seek(0)         // start
frame = 15 (@ 30fps)       -> tl.seek(0.5)       // 0.5 seconds in
frame = 30 (@ 30fps)       -> tl.seek(1.0)       // 1.0 seconds in
frame = durationInFrames-1  -> tl.seek(totalDur)  // end

Conversion:  timeInSeconds = frame / fps
             tl.seek(timeInSeconds)
```

**Important:** `tl.seek()` is what makes GSAP deterministic in Remotion. Unlike `tl.play()` which relies on requestAnimationFrame and wall-clock time, `seek()` jumps directly to a specific time position. The same frame number always produces the same visual.

### 1.3 Progress-Based Alternative

For normalized 0-1 control (useful when timeline duration is dynamic):

```tsx
useEffect(() => {
  if (!tlRef.current) return;
  const progress = frame / durationInFrames;
  tlRef.current.progress(progress);
}, [frame, durationInFrames]);
```

### 1.4 Determinism Guarantees

GSAP timelines are deterministic when:
1. **Created paused** (`{ paused: true }`)
2. **Seeked explicitly** (never `play()`, never `resume()`)
3. **No random values** in animation params (use seeded random or fixed values)
4. **No DOM-dependent calculations** at seek time (pre-calculate in build phase)
5. **No interactive plugins** (no Draggable, Observer, Inertia, ScrollTrigger)

Things that break determinism:
- `Math.random()` anywhere in timeline construction
- `gsap.utils.random()` without a seed
- `requestAnimationFrame` loops
- Anything that reads live DOM measurements per frame

### 1.5 Plugin Registration for Remotion

Register GSAP plugins once at the module level (outside React components):

```tsx
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';
import { ScrambleTextPlugin } from 'gsap/ScrambleTextPlugin';
import { TextPlugin } from 'gsap/TextPlugin';
import { CustomEase } from 'gsap/CustomEase';
import { CustomBounce } from 'gsap/CustomBounce';
import { CustomWiggle } from 'gsap/CustomWiggle';
import { Physics2DPlugin } from 'gsap/Physics2DPlugin';

gsap.registerPlugin(
  SplitText,
  DrawSVGPlugin,
  MorphSVGPlugin,
  MotionPathPlugin,
  ScrambleTextPlugin,
  TextPlugin,
  CustomEase,
  CustomBounce,
  CustomWiggle,
  Physics2DPlugin
);
```

### 1.6 Flickering Prevention in Remotion

Remotion renders frames in parallel across multiple browser tabs. To prevent flickering:

1. **Never rely on component state** that accumulates across frames
2. **Never use `useState` for animation values** -- derive everything from `useCurrentFrame()`
3. **GSAP timeline must be rebuilt identically** each time the component mounts (since parallel tabs create independent instances)
4. **Use `delayRender()` / `continueRender()`** if fonts or assets must load before GSAP can split/measure text
5. **All animations must be a pure function of frame number**

```tsx
import { delayRender, continueRender } from 'remotion';

// For SplitText: wait for fonts before splitting
function useGSAPWithFonts(buildTimeline) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);
  const [handle] = useState(() => delayRender());

  useEffect(() => {
    // Wait for fonts, then build timeline
    document.fonts.ready.then(() => {
      if (!containerRef.current) return;
      const tl = gsap.timeline({ paused: true });
      buildTimeline(tl, containerRef.current);
      tlRef.current = tl;
      continueRender(handle);
    });
    return () => { tlRef.current?.kill(); };
  }, []);

  useEffect(() => {
    if (!tlRef.current) return;
    tlRef.current.seek(frame / fps);
  }, [frame, fps]);

  return containerRef;
}
```

---

## 2. Core Animation Patterns

### 2.1 Timeline Orchestration in Remotion

```tsx
import { useCurrentFrame, useVideoConfig, AbsoluteFill } from 'remotion';

const TimelineDemo: React.FC = () => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const title = container.querySelector('.title');
    const subtitle = container.querySelector('.subtitle');
    const cta = container.querySelector('.cta');

    tl.defaults({ duration: 1, ease: "power2.out" });
    tl.from(title, { y: 50, opacity: 0 })
      .from(subtitle, { y: 30, opacity: 0 }, "-=0.5")
      .from(cta, { scale: 0, opacity: 0 }, "+=0.2");
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef}>
        <h1 className="title">Main Title</h1>
        <p className="subtitle">Subtitle text</p>
        <button className="cta">Call to Action</button>
      </div>
    </AbsoluteFill>
  );
};
```

**Position Parameter Syntax:**
| Syntax | Meaning |
|--------|---------|
| `3` | Absolute time (3s from timeline start) |
| `"+=1"` | 1 second after previous animation ends |
| `"-=0.5"` | 0.5 seconds before previous animation ends (overlap) |
| `"<"` | At the start of the previous animation |
| `"<0.5"` | 0.5 seconds after the start of the previous animation |
| `">-0.2"` | 0.2 seconds before the end of the previous animation |

**Nested Timelines as Remotion Components:**
```tsx
// Each section is its own function returning a timeline
function buildIntro(tl: gsap.core.Timeline, container: HTMLDivElement) {
  const logo = container.querySelector('.logo');
  const tagline = container.querySelector('.tagline');
  const introTl = gsap.timeline();
  introTl.from(logo, { scale: 0, rotation: -180, duration: 1 })
         .from(tagline, { y: 20, opacity: 0, duration: 0.5 });
  tl.add(introTl);
}

function buildContent(tl: gsap.core.Timeline, container: HTMLDivElement) {
  const heading = container.querySelector('.heading');
  const body = container.querySelector('.body-text');
  const contentTl = gsap.timeline();
  contentTl.from(heading, { x: -100, opacity: 0, duration: 0.6 })
           .from(body, { y: 50, opacity: 0, duration: 0.5 }, "-=0.3");
  tl.add(contentTl, "-=0.5");
}

// Master composition
const MasterScene: React.FC = () => {
  const containerRef = useGSAPTimeline((tl, container) => {
    buildIntro(tl, container);
    buildContent(tl, container);
    buildOutro(tl, container);
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef}>
        <div className="logo">LOGO</div>
        <div className="tagline">Tagline</div>
        <h1 className="heading">Heading</h1>
        <p className="body-text">Body text...</p>
      </div>
    </AbsoluteFill>
  );
};
```

**Labels for Scene Navigation:**
```tsx
// Labels can be used for programmatic navigation and debugging
const tl = gsap.timeline({ paused: true });
tl.addLabel("intro")
  .from(logo, { scale: 0, duration: 0.8 })
  .addLabel("content", "+=0.2")
  .from(text, { opacity: 0, duration: 0.6 })
  .addLabel("outro", "+=2");  // 2s hold after text

// In Remotion, seek by time, but labels help organize construction
```

### 2.2 Stagger Patterns

```tsx
const StaggerGrid: React.FC<{ items: string[] }> = ({ items }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const gridItems = container.querySelectorAll('.grid-item');
    tl.from(gridItems, {
      scale: 0,
      opacity: 0,
      duration: 0.6,
      stagger: {
        each: 0.1,
        from: "center",
        grid: [4, 6],
        ease: "power2.in"
      }
    });
  });

  return (
    <div ref={containerRef} style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)' }}>
      {items.map((item, i) => (
        <div key={i} className="grid-item">{item}</div>
      ))}
    </div>
  );
};
```

**Stagger `from` Options:**
| Value | Effect |
|-------|--------|
| `"start"` | Default, sequential from first |
| `"center"` | Radiate outward from center |
| `"edges"` | Start from both edges toward center |
| `"random"` | Random order (caution: may not be deterministic -- use fixed seed) |
| `"end"` | Reverse, from last to first |
| `5` | Start from index 5 |
| `[0.5, 0.5]` | Start from 50%/50% position in grid |

> **Remotion Warning:** `from: "random"` uses GSAP's internal random which is NOT seeded. For deterministic rendering, use a function-based stagger with seeded randomness instead:

```tsx
// Deterministic random stagger for Remotion
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

tl.from(items, {
  y: 100,
  opacity: 0,
  stagger: function(index) {
    // Deterministic "random-looking" delay
    return seededRandom(index * 7919) * 0.5;
  }
});
```

### 2.3 Easing for Motion Graphics

**Standard Eases:**
- `power1` through `power4` (light to heavy acceleration)
- `back` (slight overshoot), `elastic` (spring-like), `bounce` (bouncing)
- `circ` (circular), `expo` (exponential), `sine` (gentle sine wave)

Each has `.in`, `.out`, `.inOut` variants.

**Special Eases (EasePack):**
```tsx
// SlowMo - slow in middle, fast at edges
tl.to(el, { x: 500, ease: "slow(0.7, 0.7, false)" });

// RoughEase - jagged, organic motion
tl.to(el, { x: 100, ease: "rough({strength: 2, points: 50, clamp: true})" });

// ExpoScaleEase - exponential scaling
tl.to(el, { x: 500, ease: "expoScale(0.5, 7, power2.inOut)" });
```

**CustomEase - Arbitrary Curves:**
```tsx
CustomEase.create("myEase", "M0,0 C0.1,0.5 0.2,1 0.4,1 0.6,1 0.8,0.8 1,1");
tl.to(el, { y: -200, ease: "myEase" });
```

**CustomBounce and CustomWiggle:**
```tsx
CustomBounce.create("myBounce", { strength: 0.6, squash: 3, squashID: "myBounce-squash" });
CustomWiggle.create("myWiggle", { wiggles: 8, type: "easeOut" });

tl.to(el, { y: -200, ease: "myBounce" });
tl.to(el, { rotation: 30, ease: "myWiggle" });
```

**GSAP to Remotion Easing Equivalents:**

These GSAP eases have approximate Remotion `Easing` equivalents (useful when choosing NOT to use GSAP for simple animations):

| GSAP Easing | Remotion Easing Equivalent |
|-------------|---------------------------|
| `power1.out` | `Easing.out(Easing.quad)` |
| `power2.out` | `Easing.out(Easing.cubic)` |
| `power3.out` | `Easing.out(Easing.cubic)` |
| `back.inOut(2)` | `Easing.inOut(Easing.back(2))` |
| `elastic.out(1, 0.3)` | `Easing.out(Easing.elastic(1))` |
| `expo.out` | `Easing.out(Easing.exp)` |

However, GSAP's easing system is **far richer** than Remotion's native `Easing`. Use GSAP eases via the timeline for: `CustomEase`, `RoughEase`, `SlowMo`, `ExpoScaleEase`, `CustomBounce`, `CustomWiggle`.

**Recommended Eases for Motion Graphics:**
| Use Case | Ease |
|----------|------|
| Entrance (slide in) | `power2.out` or `power3.out` |
| Exit (slide out) | `power2.in` |
| Attention/bounce | `back.out(1.7)` |
| Smooth transition | `power1.inOut` |
| Dramatic entrance | `expo.out` |
| Organic motion | `sine.inOut` |
| Impact/hit | `power4.out` |
| Text reveal | `power2.out` or `circ.out` |
| Logo animation | `elastic.out(1, 0.5)` |
| Counter/number | `power1.out` |

---

## 3. Text Animation Patterns

### 3.1 SplitText Plugin in Remotion

SplitText manipulates the DOM to split text into individual elements. In Remotion, this must happen in `useEffect` after mount, and fonts must be loaded first.

```tsx
import { AbsoluteFill, delayRender, continueRender } from 'remotion';
import { SplitText } from 'gsap/SplitText';

const TextReveal: React.FC<{ text: string }> = ({ text }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const heading = container.querySelector('.heading');

    // SplitText modifies the DOM -- must happen after mount + font load
    const split = SplitText.create(heading, {
      type: "chars,words,lines",
      mask: "lines"  // clip mask for reveal
    });

    tl.from(split.chars, {
      y: 100,
      opacity: 0,
      duration: 0.6,
      stagger: 0.03,
      ease: "power2.out"
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

**SplitText Key Options:**
| Option | Purpose |
|--------|---------|
| `type` | `"chars"`, `"words"`, `"lines"` (comma-separated) |
| `mask` | Wrap in clip containers: `"lines"`, `"words"`, `"chars"` |
| `autoSplit` | Auto re-split on font load or resize (less useful in Remotion -- fixed size) |
| `deepSlice` | Handle nested elements like `<strong>` across lines |
| `propIndex` | Add CSS vars `--char`, `--word`, `--line` per element |
| `onSplit()` | Callback after split, ideal for animation setup |

**Text Reveal Patterns as Remotion Components:**

```tsx
// Pattern 1: Line-by-line reveal with mask
const LineReveal: React.FC<{ text: string; startFrame?: number }> = ({ text, startFrame = 0 }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const el = container.querySelector('.text');
    const split = SplitText.create(el, { type: "lines", mask: "lines" });
    tl.from(split.lines, {
      y: "100%",
      duration: 0.8,
      stagger: 0.15,
      ease: "power3.out"
    });
  });

  return (
    <div ref={containerRef}>
      <p className="text" style={{ fontSize: 48 }}>{text}</p>
    </div>
  );
};

// Pattern 2: Character cascade with 3D rotation
const CharCascade: React.FC<{ text: string }> = ({ text }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const el = container.querySelector('.title');
    const split = SplitText.create(el, { type: "chars" });
    tl.from(split.chars, {
      y: 50,
      opacity: 0,
      rotationX: -90,
      transformPerspective: 600,
      duration: 0.5,
      stagger: 0.02,
      ease: "back.out(1.7)"
    });
  });

  return (
    <div ref={containerRef}>
      <h1 className="title" style={{ fontSize: 72 }}>{text}</h1>
    </div>
  );
};

// Pattern 3: Word-by-word scale
const WordScale: React.FC<{ text: string }> = ({ text }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const el = container.querySelector('.subtitle');
    const split = SplitText.create(el, { type: "words" });
    tl.from(split.words, {
      scale: 0,
      opacity: 0,
      duration: 0.4,
      stagger: 0.08,
      ease: "back.out(2)"
    });
  });

  return (
    <div ref={containerRef}>
      <h2 className="subtitle" style={{ fontSize: 48 }}>{text}</h2>
    </div>
  );
};
```

### 3.2 ScrambleText Plugin in Remotion

**Important Determinism Note:** ScrambleText uses internal randomness for character selection. In Remotion's parallel rendering, this can cause different random characters on different tabs. The visual result is generally acceptable since the final resolved text is deterministic and the scramble is inherently "random-looking", but frame-exact reproducibility requires `--concurrency=1`.

```tsx
const ScrambleReveal: React.FC<{ text: string }> = ({ text }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const el = container.querySelector('.scramble-text');
    tl.to(el, {
      duration: 2,
      scrambleText: {
        text: text,
        chars: "01",          // binary decode effect
        revealDelay: 0.5,
        speed: 0.3,
        newClass: "revealed"
      }
    });
  });

  return (
    <div ref={containerRef}>
      <p className="scramble-text" style={{ fontFamily: 'monospace', fontSize: 36 }}>
        {'X'.repeat(text.length)}
      </p>
    </div>
  );
};
```

**Character Set Options:**
- `"upperCase"` - A-Z
- `"lowerCase"` - a-z
- `"upperAndLowerCase"` - A-Za-z
- `"01"` - binary
- Custom string like `"!@#$%^&*()"` or Japanese characters

### 3.3 TextPlugin in Remotion

```tsx
const Typewriter: React.FC<{ text: string; duration?: number }> = ({ text, duration = 3 }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const el = container.querySelector('.typewriter');
    tl.to(el, {
      duration,
      text: text,
      ease: "none"  // linear for typewriter effect
    });
  });

  return (
    <div ref={containerRef}>
      <p className="typewriter" style={{ fontFamily: 'monospace', fontSize: 24 }}></p>
    </div>
  );
};

// Word-by-word variant
const WordByWord: React.FC<{ text: string }> = ({ text }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const el = container.querySelector('.text');
    tl.to(el, {
      duration: 3,
      text: { value: text, delimiter: " " },
      ease: "none"
    });
  });

  return (
    <div ref={containerRef}>
      <p className="text" style={{ fontSize: 32 }}></p>
    </div>
  );
};
```

### 3.4 Kinetic Typography as Remotion Composition

```tsx
import { Composition, Sequence, AbsoluteFill } from 'remotion';

const KineticTypography: React.FC<{
  lines: string[];
  style?: 'cascade' | 'impact' | 'wave';
}> = ({ lines, style = 'cascade' }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    lines.forEach((line, i) => {
      const el = container.querySelector(`.line-${i}`);
      if (!el) return;
      const split = SplitText.create(el, {
        type: "words,chars",
        mask: "words"
      });

      // Entrance
      tl.from(split.words, {
        y: "100%",
        duration: 0.6,
        stagger: 0.08,
        ease: "power3.out"
      }, i * 1.5)
      // Hold for reading
      .to({}, { duration: 1 })
      // Exit (if not last line)
      if (i < lines.length - 1) {
        tl.to(split.words, {
          y: "-100%",
          opacity: 0,
          duration: 0.4,
          stagger: 0.04,
          ease: "power2.in"
        });
      }
    });
  });

  return (
    <AbsoluteFill style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#000', color: '#fff'
    }}>
      <div ref={containerRef}>
        {lines.map((line, i) => (
          <h1 key={i} className={`line-${i}`}
              style={{ fontSize: 72, position: 'absolute', textAlign: 'center' }}>
            {line}
          </h1>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 4. SVG/Shape Animation Patterns

### 4.1 MorphSVG Plugin in Remotion

```tsx
const ShapeMorph: React.FC<{ shapes: string[] }> = ({ shapes }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const path = container.querySelector('#morph-path');

    // Sequence through shapes
    shapes.forEach((shape, i) => {
      if (i === 0) return; // first shape is the starting state
      tl.to(path, {
        morphSVG: {
          shape: shape,      // SVG path data string
          type: "rotational",
          map: "size"
        },
        duration: 1,
        ease: "power2.inOut"
      }, `+=${i === 1 ? 0 : 0.5}`);
    });
  });

  return (
    <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef}>
        <svg viewBox="0 0 500 500" width={400} height={400}>
          <path id="morph-path" d={shapes[0]} fill="#3b82f6" />
        </svg>
      </div>
    </AbsoluteFill>
  );
};
```

**MorphSVG Configuration:**
| Option | Purpose |
|--------|---------|
| `shape` | Target path data or selector |
| `type` | `"linear"` (default) or `"rotational"` |
| `shapeIndex` | Point alignment offset |
| `map` | Segment matching: `"size"`, `"position"`, `"complexity"` |
| `origin` | Rotation origin for rotational type |
| `precision` | Decimal places for output (default: 2) |

### 4.2 DrawSVG Plugin in Remotion

```tsx
const LogoDraw: React.FC<{ svgPaths: React.ReactNode }> = ({ svgPaths }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const paths = container.querySelectorAll('.draw-path');

    // Draw each path sequentially
    tl.from(paths, {
      drawSVG: 0,
      duration: 1.5,
      stagger: 0.2,
      ease: "power2.inOut"
    })
    // Fill in after drawing
    .to(paths, {
      fill: "#ffffff",
      duration: 0.5,
      stagger: 0.1
    }, "-=0.3");
  });

  return (
    <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#000' }}>
      <div ref={containerRef}>
        <svg viewBox="0 0 200 200" width={400} height={400}>
          {svgPaths}
        </svg>
      </div>
    </AbsoluteFill>
  );
};
```

**DrawSVG Patterns:**
```tsx
// Draw from nothing
tl.from(path, { drawSVG: 0, duration: 2 });

// Draw from center outward
tl.from(path, { drawSVG: "50% 50%", duration: 2 });

// Show only a segment
tl.to(path, { drawSVG: "20% 80%", duration: 2 });

// Erase effect (draw to nothing)
tl.to(path, { drawSVG: "100% 100%", duration: 1 });
```

### 4.3 MotionPath Plugin in Remotion

```tsx
const PathFollower: React.FC = () => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const element = container.querySelector('.follower');
    const path = container.querySelector('#motion-path');

    tl.to(element, {
      motionPath: {
        path: path as SVGPathElement,
        align: path as SVGPathElement,
        alignOrigin: [0.5, 0.5],
        autoRotate: true
      },
      duration: 3,
      ease: "power1.inOut"
    });
  });

  return (
    <div ref={containerRef} style={{ position: 'relative', width: '100%', height: '100%' }}>
      <svg style={{ position: 'absolute', width: '100%', height: '100%' }}>
        <path id="motion-path" d="M 100,300 C 200,100 400,100 500,300"
              fill="none" stroke="#333" strokeWidth={2} />
      </svg>
      <div className="follower" style={{
        width: 20, height: 20, borderRadius: '50%',
        background: '#3b82f6', position: 'absolute'
      }} />
    </div>
  );
};
```

### 4.4 SVG Filter Animations in Remotion

```tsx
const BlurReveal: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const blur = container.querySelector('#blur');
    tl.fromTo(blur,
      { attr: { stdDeviation: 20 } },
      { attr: { stdDeviation: 0 }, duration: 1.5, ease: "power2.out" }
    );
  });

  return (
    <div ref={containerRef}>
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <defs>
          <filter id="blur-filter">
            <feGaussianBlur id="blur" stdDeviation="20" />
          </filter>
        </defs>
      </svg>
      <div style={{ filter: 'url(#blur-filter)' }}>
        {children}
      </div>
    </div>
  );
};
```

---

## 5. Transition Effects

### 5.1 Clip-Path Transitions as Remotion Components

```tsx
type TransitionType = 'circleReveal' | 'wipeLeft' | 'wipeRight' | 'irisReveal' | 'blinds';

const ClipPathTransition: React.FC<{
  type: TransitionType;
  children: React.ReactNode;
}> = ({ type, children }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const scene = container.querySelector('.scene');
    const transitions: Record<TransitionType, [string, string]> = {
      circleReveal: [
        "circle(0% at 50% 50%)",
        "circle(75% at 50% 50%)"
      ],
      wipeLeft: [
        "polygon(0 0, 0 0, 0 100%, 0 100%)",
        "polygon(0 0, 100% 0, 100% 100%, 0 100%)"
      ],
      wipeRight: [
        "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)",
        "polygon(0 0, 100% 0, 100% 100%, 0 100%)"
      ],
      irisReveal: [
        "polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)",
        "polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)"
      ],
      blinds: [
        "inset(0 0 100% 0)",
        "inset(0 0 0% 0)"
      ]
    };

    const [from, to] = transitions[type];
    tl.fromTo(scene,
      { clipPath: from },
      { clipPath: to, duration: 0.8, ease: "power2.inOut" }
    );
  });

  return (
    <div ref={containerRef}>
      <div className="scene">{children}</div>
    </div>
  );
};
```

### 5.2 Scene Transitions Between Sequences

```tsx
import { Sequence, AbsoluteFill } from 'remotion';

// Slide transition wrapper
const SlideTransition: React.FC<{
  direction?: 'left' | 'right' | 'up' | 'down';
  outgoing: React.ReactNode;
  incoming: React.ReactNode;
  transitionDuration?: number; // in frames
}> = ({ direction = 'left', outgoing, incoming, transitionDuration = 15 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const containerRef = useGSAPTimeline((tl, container) => {
    const out = container.querySelector('.outgoing');
    const inc = container.querySelector('.incoming');

    const axis = (direction === 'left' || direction === 'right') ? 'x' : 'y';
    const outVal = (direction === 'left' || direction === 'up') ? '-100%' : '100%';
    const inVal = (direction === 'left' || direction === 'up') ? '100%' : '-100%';

    tl.to(out, { [axis]: outVal, duration: transitionDuration / fps, ease: "power2.inOut" })
      .fromTo(inc,
        { [axis]: inVal },
        { [axis]: '0%', duration: transitionDuration / fps, ease: "power2.inOut" },
        0
      );
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef} style={{ width: '100%', height: '100%', position: 'relative' }}>
        <div className="outgoing" style={{ position: 'absolute', inset: 0 }}>{outgoing}</div>
        <div className="incoming" style={{ position: 'absolute', inset: 0 }}>{incoming}</div>
      </div>
    </AbsoluteFill>
  );
};
```

### 5.3 Crossfade / Dissolve

```tsx
const Crossfade: React.FC<{
  outgoing: React.ReactNode;
  incoming: React.ReactNode;
  durationSec?: number;
}> = ({ outgoing, incoming, durationSec = 1 }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const out = container.querySelector('.outgoing');
    const inc = container.querySelector('.incoming');

    tl.to(out, { opacity: 0, duration: durationSec })
      .fromTo(inc, { opacity: 0 }, { opacity: 1, duration: durationSec }, 0);
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef} style={{ width: '100%', height: '100%', position: 'relative' }}>
        <div className="outgoing" style={{ position: 'absolute', inset: 0 }}>{outgoing}</div>
        <div className="incoming" style={{ position: 'absolute', inset: 0 }}>{incoming}</div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## 6. Motion Graphics Templates (Remotion Compositions)

### 6.1 Lower Third Composition

```tsx
const LowerThird: React.FC<{
  name: string;
  title: string;
  holdDuration?: number; // seconds
  accentColor?: string;
}> = ({ name, title, holdDuration = 4, accentColor = '#3b82f6' }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const bar = container.querySelector('.lt-bar');
    const nameEl = container.querySelector('.lt-name');
    const titleEl = container.querySelector('.lt-title');
    const accent = container.querySelector('.lt-accent');

    // Entrance
    tl.fromTo(bar,
      { scaleX: 0, transformOrigin: "left center" },
      { scaleX: 1, duration: 0.4, ease: "power2.out" }
    )
    .from(nameEl, { x: -30, opacity: 0, duration: 0.3, ease: "power2.out" }, "-=0.1")
    .from(titleEl, { x: -20, opacity: 0, duration: 0.3, ease: "power2.out" }, "-=0.1")
    .from(accent, {
      scaleX: 0, transformOrigin: "left", duration: 0.3, ease: "power2.out"
    }, "-=0.2")
    // Hold
    .to({}, { duration: holdDuration })
    // Exit
    .to([bar, nameEl, titleEl, accent], {
      x: -50, opacity: 0, duration: 0.3, ease: "power2.in", stagger: 0.05
    });
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef} style={{ position: 'absolute', bottom: 80, left: 60 }}>
        <div className="lt-bar" style={{
          background: accentColor, padding: '12px 24px',
          borderRadius: 4, minWidth: 300
        }}>
          <div className="lt-name" style={{ fontSize: 28, fontWeight: 'bold', color: '#fff' }}>
            {name}
          </div>
          <div className="lt-title" style={{ fontSize: 18, color: 'rgba(255,255,255,0.8)' }}>
            {title}
          </div>
        </div>
        <div className="lt-accent" style={{
          height: 3, background: '#fff', marginTop: 4, width: 60
        }} />
      </div>
    </AbsoluteFill>
  );
};

// Register as Remotion Composition
// <Composition id="LowerThird" component={LowerThird}
//   durationInFrames={210} fps={30} width={1920} height={1080}
//   defaultProps={{ name: "John Doe", title: "CEO, Company" }} />
```

### 6.2 Title Card Composition

```tsx
const TitleCard: React.FC<{
  mainTitle: string;
  subtitle?: string;
  bgColor?: string;
}> = ({ mainTitle, subtitle, bgColor = '#0f172a' }) => {
  const containerRef = useGSAPWithFonts((tl, container) => {
    const bgShape = container.querySelector('.bg-shape');
    const titleEl = container.querySelector('.main-title');
    const subtitleEl = container.querySelector('.subtitle');
    const divider = container.querySelector('.divider');

    // Background shape
    tl.from(bgShape, { scale: 0, rotation: -45, duration: 0.8, ease: "back.out(1.7)" });

    // Split + animate title
    const split = SplitText.create(titleEl, { type: "chars", mask: "chars" });
    tl.from(split.chars, {
      y: "100%",
      duration: 0.5,
      stagger: 0.03,
      ease: "power3.out"
    }, "-=0.3");

    // Subtitle
    if (subtitleEl) {
      tl.from(subtitleEl, { y: 20, opacity: 0, duration: 0.6, ease: "power2.out" }, "-=0.2");
    }

    // Divider line
    tl.from(divider, { scaleX: 0, duration: 0.4, ease: "power2.out" }, "-=0.3");
  });

  return (
    <AbsoluteFill style={{ background: bgColor, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef} style={{ textAlign: 'center', color: '#fff' }}>
        <div className="bg-shape" style={{
          position: 'absolute', width: 200, height: 200, borderRadius: '50%',
          background: 'rgba(59,130,246,0.2)', top: '30%', left: '45%'
        }} />
        <h1 className="main-title" style={{ fontSize: 80, fontWeight: 'bold', position: 'relative' }}>
          {mainTitle}
        </h1>
        <div className="divider" style={{
          width: 80, height: 3, background: '#3b82f6', margin: '20px auto'
        }} />
        {subtitle && (
          <p className="subtitle" style={{ fontSize: 32, opacity: 0.8 }}>{subtitle}</p>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

### 6.3 Logo Reveal Composition

```tsx
const LogoReveal: React.FC<{
  logoSvgPaths: React.ReactNode;
  logoText?: string;
  variant?: 'draw' | 'scale' | 'morph';
}> = ({ logoSvgPaths, logoText, variant = 'draw' }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    if (variant === 'draw') {
      const paths = container.querySelectorAll('.logo-path');
      tl.from(paths, { drawSVG: 0, duration: 1.5, stagger: 0.1, ease: "power2.inOut" })
        .to(paths, { fill: "#ffffff", duration: 0.5 }, "-=0.3");
    } else if (variant === 'scale') {
      const logo = container.querySelector('.logo-container');
      tl.from(logo, { scale: 0, rotation: -180, duration: 1, ease: "back.out(1.7)" });
    }

    if (logoText) {
      const text = container.querySelector('.logo-text');
      tl.from(text, { opacity: 0, x: -20, duration: 0.5, ease: "power2.out" }, "-=0.2");
    }
  });

  return (
    <AbsoluteFill style={{ background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef} style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
        <div className="logo-container">
          <svg viewBox="0 0 100 100" width={120} height={120}>
            {logoSvgPaths}
          </svg>
        </div>
        {logoText && (
          <span className="logo-text" style={{ fontSize: 48, color: '#fff', fontWeight: 'bold' }}>
            {logoText}
          </span>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

### 6.4 Counter / Data Visualization Composition

```tsx
const AnimatedCounter: React.FC<{
  endValue: number;
  prefix?: string;
  suffix?: string;
  durationSec?: number;
}> = ({ endValue, prefix = '', suffix = '', durationSec = 2 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const [displayValue, setDisplayValue] = useState('0');

  // Use GSAP to tween a proxy object, read its value on each frame
  const proxyRef = useRef({ value: 0 });
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    const tl = gsap.timeline({ paused: true });
    tl.to(proxyRef.current, {
      value: endValue,
      duration: durationSec,
      ease: "power1.out"
    });
    tlRef.current = tl;
    return () => { tl.kill(); };
  }, [endValue, durationSec]);

  useEffect(() => {
    if (!tlRef.current) return;
    tlRef.current.seek(frame / fps);
    setDisplayValue(Math.round(proxyRef.current.value).toLocaleString());
  }, [frame, fps]);

  return (
    <div ref={containerRef} style={{
      fontSize: 96, fontWeight: 'bold', fontVariantNumeric: 'tabular-nums'
    }}>
      {prefix}{displayValue}{suffix}
    </div>
  );
};

// Bar chart animation
const AnimatedBarChart: React.FC<{ data: { label: string; value: number; color: string }[] }> = ({ data }) => {
  const maxValue = Math.max(...data.map(d => d.value));

  const containerRef = useGSAPTimeline((tl, container) => {
    const bars = container.querySelectorAll('.bar');
    tl.from(bars, {
      scaleY: 0,
      transformOrigin: "bottom",
      duration: 0.8,
      stagger: 0.1,
      ease: "power2.out"
    });
  });

  return (
    <div ref={containerRef} style={{ display: 'flex', alignItems: 'flex-end', gap: 16, height: 300 }}>
      {data.map((d, i) => (
        <div key={i} style={{ textAlign: 'center' }}>
          <div className="bar" style={{
            width: 60, height: (d.value / maxValue) * 250,
            background: d.color, borderRadius: '4px 4px 0 0'
          }} />
          <span style={{ fontSize: 14, marginTop: 8 }}>{d.label}</span>
        </div>
      ))}
    </div>
  );
};
```

### 6.5 End Screen / Outro Composition

```tsx
const EndScreen: React.FC<{
  channelName: string;
  socialLinks: { icon: string; label: string }[];
  ctaText?: string;
}> = ({ channelName, socialLinks, ctaText = 'Subscribe' }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const bg = container.querySelector('.outro-bg');
    const icons = container.querySelectorAll('.social-icon');
    const cta = container.querySelector('.cta-text');
    const name = container.querySelector('.channel-name');

    tl.from(bg, { opacity: 0, duration: 0.3 })
      .from(icons, {
        scale: 0, opacity: 0, duration: 0.4,
        stagger: 0.1, ease: "back.out(1.7)"
      })
      .from(cta, { y: 20, opacity: 0, duration: 0.4 })
      .from(name, { opacity: 0, duration: 0.3 });
  });

  return (
    <AbsoluteFill>
      <div ref={containerRef} style={{
        width: '100%', height: '100%',
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center'
      }}>
        <div className="outro-bg" style={{
          position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.9)'
        }} />
        <div style={{ position: 'relative', textAlign: 'center' }}>
          <div style={{ display: 'flex', gap: 24, marginBottom: 32 }}>
            {socialLinks.map((link, i) => (
              <div key={i} className="social-icon" style={{
                width: 48, height: 48, borderRadius: '50%',
                background: '#333', display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: '#fff', fontSize: 20
              }}>
                {link.icon}
              </div>
            ))}
          </div>
          <p className="cta-text" style={{ fontSize: 32, color: '#fff', marginBottom: 16 }}>{ctaText}</p>
          <p className="channel-name" style={{ fontSize: 24, color: '#999' }}>{channelName}</p>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### 6.6 Composition Registration Pattern

```tsx
import { Composition } from 'remotion';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TitleCard"
        component={TitleCard}
        durationInFrames={120}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ mainTitle: "HELLO WORLD", subtitle: "A GSAP Motion Story" }}
      />
      <Composition
        id="LowerThird"
        component={LowerThird}
        durationInFrames={210}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ name: "Jane Smith", title: "Creative Director" }}
      />
      <Composition
        id="LogoReveal"
        component={LogoReveal}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          logoSvgPaths: <circle className="logo-path" cx={50} cy={50} r={40} fill="none" stroke="#fff" strokeWidth={2} />,
          logoText: "BRAND"
        }}
      />
      {/* Social media format variants */}
      <Composition
        id="IGStory-TitleCard"
        component={TitleCard}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ mainTitle: "SWIPE UP", subtitle: "Link in bio" }}
      />
    </>
  );
};
```

---

## 7. Advanced Techniques

### 7.1 Physics-Based Animations in Remotion

Physics2D plugin creates non-interactive physics. It builds a deterministic timeline internally, so it works with `seek()`.

```tsx
const ParticleBurst: React.FC<{ count?: number }> = ({ count = 20 }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const particles = container.querySelectorAll('.particle');
    particles.forEach((p, i) => {
      // Use seeded values for determinism
      const angle = (360 / count) * i + (i % 3) * 15;
      const velocity = 200 + (i % 5) * 40;

      tl.to(p, {
        physics2D: {
          velocity,
          angle,
          gravity: 300
        },
        opacity: 0,
        duration: 2
      }, 0);
    });
  });

  return (
    <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div ref={containerRef} style={{ position: 'relative' }}>
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="particle" style={{
            position: 'absolute', width: 8, height: 8,
            borderRadius: '50%',
            background: `hsl(${(i * 360) / count}, 70%, 60%)`
          }} />
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

### 7.2 3D Transforms and Perspective

```tsx
const Card3DFlip: React.FC<{
  front: React.ReactNode;
  back: React.ReactNode;
}> = ({ front, back }) => {
  const containerRef = useGSAPTimeline((tl, container) => {
    const card = container.querySelector('.card');

    gsap.set(container, { perspective: 800 });
    tl.to(card, { rotationY: 180, duration: 0.8, ease: "power2.inOut" });
  });

  return (
    <div ref={containerRef}>
      <div className="card" style={{ transformStyle: 'preserve-3d', position: 'relative' }}>
        <div style={{ backfaceVisibility: 'hidden' }}>{front}</div>
        <div style={{
          backfaceVisibility: 'hidden', transform: 'rotateY(180deg)',
          position: 'absolute', inset: 0
        }}>{back}</div>
      </div>
    </div>
  );
};
```

### 7.3 Color / Gradient Transitions

```tsx
const GradientShift: React.FC<{
  fromColors: [string, string];
  toColors: [string, string];
  angle?: number;
  children: React.ReactNode;
}> = ({ fromColors, toColors, angle = 45, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bgRef = useRef<HTMLDivElement>(null);
  const proxyRef = useRef({ c1: fromColors[0], c2: fromColors[1] });
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    const tl = gsap.timeline({ paused: true });
    tl.to(proxyRef.current, {
      c1: toColors[0], c2: toColors[1],
      duration: 2, ease: "power1.inOut"
    });
    tlRef.current = tl;
    return () => { tl.kill(); };
  }, []);

  useEffect(() => {
    if (!tlRef.current || !bgRef.current) return;
    tlRef.current.seek(frame / fps);
    bgRef.current.style.background =
      `linear-gradient(${angle}deg, ${proxyRef.current.c1}, ${proxyRef.current.c2})`;
  }, [frame, fps]);

  return (
    <AbsoluteFill ref={bgRef}>
      {children}
    </AbsoluteFill>
  );
};
```

### 7.4 Performance Optimization for Remotion

1. **Animate transforms and opacity only** (GPU-accelerated via `force3D: true`)
2. **Use `gsap.set()` for initial states** in the timeline build phase
3. **Pre-split text once** in useEffect, not per frame
4. **Avoid re-creating timelines** -- build once, seek on every frame
5. **Precompile MorphSVG paths** for complex morphs
6. **Minimize DOM element count** -- 50+ animated elements may be slow
7. **Use `will-change: transform`** on animated containers

```tsx
// Anti-pattern: rebuilding timeline per frame
// useEffect(() => {
//   const tl = gsap.timeline(); // BAD: recreates every frame
//   tl.to(el, { x: 100 });
//   tl.seek(frame / fps);
// }, [frame]);

// Correct: build once, seek per frame
useEffect(() => {
  const tl = gsap.timeline({ paused: true });
  tl.to(el, { x: 100 });
  tlRef.current = tl;
  return () => tl.kill();
}, []);  // empty deps = build once

useEffect(() => {
  tlRef.current?.seek(frame / fps);
}, [frame, fps]);  // seek every frame
```

---

## 8. GSAP Plugins Reference

All plugins are now **free** (including former Club GreenSock plugins).

### Plugins Relevant for Remotion Video Production

| Plugin | Purpose | Remotion Compatible | Notes |
|--------|---------|:-------------------:|-------|
| **SplitText** | Split text for animation | Yes | Use `delayRender` for font loading |
| **ScrambleText** | Character scramble | Mostly | Internal randomness not seeded |
| **TextPlugin** | Character replacement | Yes | Fully deterministic |
| **DrawSVG** | SVG stroke animation | Yes | Fully deterministic |
| **MorphSVG** | Shape morphing | Yes | Fully deterministic |
| **MotionPath** | Path-following | Yes | Fully deterministic |
| **CustomEase** | Custom easing curves | Yes | Fully deterministic |
| **EasePack** | RoughEase, SlowMo | Mostly | RoughEase has internal randomness |
| **CustomBounce** | Bounce physics | Yes | Fully deterministic |
| **CustomWiggle** | Wiggle/shake | Yes | Fully deterministic |
| **Physics2D** | 2D physics | Yes | Deterministic with fixed params |
| **PhysicsProps** | Per-property physics | Yes | Deterministic with fixed params |
| **Flip** | Layout transitions | Caution | Reads live DOM -- use carefully |
| **Pixi** | PixiJS integration | Possible | Complex setup with Remotion |

### Not Recommended for Remotion

| Plugin | Reason |
|--------|--------|
| **ScrollTrigger** | No scrolling in video |
| **ScrollTo** | No scrolling in video |
| **ScrollSmoother** | No scrolling in video |
| **Draggable** | Interactive only |
| **Inertia** | Interactive only |
| **Observer** | Event-based only |
| **MotionPathHelper** | Dev tool only |
| **GSDevTools** | Dev tool only |

### Plugin Tiers for Video Production

**Tier 1 (Essential):**
- `gsap.timeline()` (core) - orchestration backbone
- `SplitText` - text animations (the primary differentiator vs Remotion-native)
- `CustomEase` / `EasePack` - motion feel beyond Remotion's `Easing`

**Tier 2 (Highly Useful):**
- `DrawSVG` - logo/line reveals
- `MorphSVG` - shape transitions (impossible without GSAP)
- `MotionPath` - path-following motion
- `ScrambleText` - decode effects
- `TextPlugin` - typewriter effects

**Tier 3 (Specialized):**
- `Physics2D` / `PhysicsProps` - particle effects
- `CustomBounce` / `CustomWiggle` - bouncing/shaking

---

## 9. Utility Functions

```tsx
// These utilities are useful in the timeline BUILD phase (not per-frame)

// Deterministic "random" for Remotion (seeded)
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

// Clamp to range
gsap.utils.clamp(0, 100, 150);  // 100

// Map from one range to another
gsap.utils.mapRange(0, 100, 0, 1, 50);  // 0.5

// Wrap around (for infinite loops)
gsap.utils.wrap(0, 100, 120);  // 20

// Snap to nearest value
gsap.utils.snap(10, 23);  // 20

// Interpolate between values (including colors)
gsap.utils.interpolate(0, 100, 0.5);  // 50
gsap.utils.interpolate("red", "blue", 0.5);  // interpolated color

// Pipe utilities together
const transform = gsap.utils.pipe(
  gsap.utils.clamp(0, 1),
  gsap.utils.mapRange(0, 1, -200, 200),
  gsap.utils.snap(10)
);

// Convert NodeList to Array
gsap.utils.toArray(".items");
```

**Warning:** `gsap.utils.random()` is NOT deterministic. In Remotion, always use `seededRandom()` or fixed values.

---

## 10. Reusable Effects System

`gsap.registerEffect()` creates named, reusable animation presets. Register effects at module level (outside components) so all Remotion compositions can use them.

```tsx
// lib/gsap-effects.ts -- import once in your Remotion project

import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';

// Register all GSAP plugins
gsap.registerPlugin(SplitText /*, ... */);

// --- Effect Definitions ---

gsap.registerEffect({
  name: "fadeIn",
  effect: (targets, config) => gsap.from(targets, {
    duration: config.duration, opacity: 0, y: config.y,
    stagger: config.stagger, ease: config.ease
  }),
  defaults: { duration: 0.8, y: 30, stagger: 0.1, ease: "power2.out" },
  extendTimeline: true
});

gsap.registerEffect({
  name: "slideIn",
  effect: (targets, config) => gsap.from(targets, {
    duration: config.duration, x: config.x, opacity: 0, ease: config.ease
  }),
  defaults: { duration: 0.6, x: -100, ease: "power2.out" },
  extendTimeline: true
});

gsap.registerEffect({
  name: "scaleReveal",
  effect: (targets, config) => gsap.from(targets, {
    duration: config.duration, scale: 0, opacity: 0, ease: config.ease
  }),
  defaults: { duration: 0.5, ease: "back.out(1.7)" },
  extendTimeline: true
});

gsap.registerEffect({
  name: "textReveal",
  effect: (targets, config) => {
    const split = SplitText.create(targets, { type: "lines", mask: "lines" });
    return gsap.from(split.lines, {
      duration: config.duration, y: "100%",
      stagger: config.stagger, ease: config.ease
    });
  },
  defaults: { duration: 0.6, stagger: 0.15, ease: "power3.out" },
  extendTimeline: true
});

gsap.registerEffect({
  name: "charCascade",
  effect: (targets, config) => {
    const split = SplitText.create(targets, { type: "chars" });
    return gsap.from(split.chars, {
      duration: config.duration, y: 50, opacity: 0,
      stagger: config.stagger, ease: config.ease
    });
  },
  defaults: { duration: 0.5, stagger: 0.03, ease: "back.out(1.7)" },
  extendTimeline: true
});

gsap.registerEffect({
  name: "wipeIn",
  effect: (targets, config) => gsap.fromTo(targets,
    { clipPath: `inset(0 ${config.direction === 'left' ? '100%' : '0'} 0 ${config.direction === 'right' ? '100%' : '0'})` },
    { clipPath: "inset(0 0% 0 0%)", duration: config.duration, ease: config.ease }
  ),
  defaults: { duration: 0.8, direction: 'left', ease: "power2.inOut" },
  extendTimeline: true
});

// --- Usage in Remotion Components ---

// After importing this file, use effects fluently in timeline construction:
// tl.textReveal(".title")
//   .fadeIn(".subtitle", { y: 20 }, "-=0.3")
//   .slideIn(".panel", { x: 200 })
//   .charCascade(".highlight");
```

---

## 11. GSAP vs After Effects

### After Effects Patterns -> GSAP + Remotion Equivalents

| After Effects | GSAP + Remotion Equivalent |
|---------------|---------------------------|
| Keyframes | `gsap.to()` / `gsap.fromTo()` in timeline |
| Pre-compose | Nested timelines or `<Sequence>` components |
| Expressions | JavaScript functions / React props |
| Ease curves | `CustomEase` with SVG paths |
| Text animators | `SplitText` + stagger |
| Shape layers | SVG + `MorphSVG` |
| Mask reveals | `clipPath` animation |
| Write-on effect | `DrawSVG` |
| Time remapping | `tl.timeScale()` or `tl.seek()` |
| Wiggle expression | `CustomWiggle` or `RoughEase` |
| 3D layers | CSS 3D transforms + `perspective` |
| Particle world | `Physics2D` + React element arrays |
| Track matte | CSS `mask` or `clipPath` |
| Blur transition | Animate `filter: blur()` via timeline |
| Displacement map | SVG `feDisplacementMap` attr animation |
| Composition | Remotion `<Composition>` |
| Render queue | Remotion CLI `npx remotion render` |

### Advantages of GSAP + Remotion Over After Effects

1. **Parametric**: Props-driven compositions, change one prop to update everything
2. **Data-driven**: Fetch from API, generate from JSON (personalized videos)
3. **Programmatic**: React loops/conditionals for dynamic content
4. **Version controlled**: Git-friendly, code review, CI/CD
5. **Composable**: React components + GSAP timelines = modular system
6. **Free**: Both GSAP and Remotion are free for most use cases
7. **Web-native**: Same tech stack as your web app
8. **Batch rendering**: `npx remotion render` with different props per video
9. **Cloud rendering**: Remotion Lambda for serverless batch production
10. **Type-safe**: TypeScript for animation parameters

---

## 12. Design Implications for Skill

### Architecture: GSAP Inside Remotion Components

The skill should provide:

**1. Core Hook (`useGSAPTimeline`):**
- Manages timeline lifecycle (create paused, seek per frame, cleanup)
- Handles font loading for SplitText via `delayRender`
- Ensures deterministic rendering

**2. Pre-registered Effects Library:**
- `fadeIn`, `slideIn`, `scaleReveal`, `textReveal`, `charCascade`, `wipeIn`
- All registered with `extendTimeline: true` for fluent `tl.fadeIn()` API
- Parameterized via config objects

**3. Template Compositions (Remotion `<Composition>`):**
- `TitleCard` -- intro with split text + background elements
- `LowerThird` -- name/title overlay with entrance/hold/exit
- `LogoReveal` -- DrawSVG or scale-based logo animation
- `SceneTransition` -- clip-path, slide, zoom, crossfade
- `AnimatedCounter` -- number count-up for data viz
- `EndScreen` -- outro with social links
- `KineticTypography` -- multi-line text sequences

**4. Animation Primitives as React Components:**
Each primitive wraps `useGSAPTimeline` and accepts props:
- `<FadeIn>`, `<SlideIn>`, `<ScaleReveal>`
- `<TextReveal>`, `<CharCascade>`, `<ScrambleReveal>`
- `<DrawPath>`, `<MorphShape>`, `<FollowPath>`
- `<ClipReveal>`, `<GradientShift>`

**5. Timing Conventions (default props):**
| Animation | Duration | Ease |
|-----------|----------|------|
| Standard entrance | 0.5-0.8s | `power2.out` |
| Standard exit | 0.3-0.5s | `power2.in` |
| Text stagger (char) | 0.02-0.05s each | `power2.out` |
| Text stagger (word) | 0.08-0.15s each | `power3.out` |
| Text stagger (line) | 0.1-0.2s each | `power3.out` |
| Scene transition | 0.5-1.0s | `power2.inOut` |
| Hold for reading | 2-4s | - |
| Lower third total | 4-6s | - |
| Logo reveal | 1.5-2.5s | `power2.inOut` |

**6. Determinism Checklist:**
- [ ] Timeline created with `{ paused: true }`
- [ ] Timeline seeked via `tl.seek(frame / fps)`, never `tl.play()`
- [ ] No `Math.random()` or `gsap.utils.random()` -- use `seededRandom()`
- [ ] Fonts loaded before `SplitText` via `delayRender()` + `document.fonts.ready`
- [ ] No interactive plugins (Draggable, Observer, ScrollTrigger)
- [ ] No DOM measurements that change between renders
- [ ] All animation values derived from props or constants

**7. Why GSAP Over Pure Remotion `interpolate()`:**

GSAP provides capabilities that are difficult/impossible with Remotion's native animation:
- **SplitText**: Automatic text splitting into chars/words/lines with masking
- **MorphSVG**: Shape-to-shape morphing with point interpolation
- **DrawSVG**: SVG stroke drawing with partial segment control
- **MotionPath**: Path-following with auto-rotation
- **ScrambleText**: Character decode effects
- **Stagger system**: Grid-aware, center/edges/random distribution
- **CustomEase**: Arbitrary SVG-path-based easing curves
- **Timeline orchestration**: Position parameters, labels, nesting, defaults
- **registerEffect**: Named, reusable, parameterized animation presets
- **Physics2D**: Velocity/gravity/friction simulation

For simple fade/slide/scale, Remotion's `interpolate()` + `spring()` is sufficient. GSAP shines for **complex, multi-element, orchestrated** motion graphics.
