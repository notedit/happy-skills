---
name: plugin-guide
description: GSAP plugin compatibility and usage patterns within Remotion
metadata:
  tags: gsap, plugins, remotion, SplitText, MorphSVG, DrawSVG, MotionPath, CustomEase
---

## Plugin Compatibility Matrix

All GSAP plugins are **100% free** since Webflow's 2024 acquisition.

### Fully Compatible (Remotion-safe)

| Plugin | Purpose | Video Use Case |
|--------|---------|----------------|
| **SplitText** | Split text into chars/words/lines | Title reveals, kinetic typography |
| **MorphSVG** | Shape-to-shape morphing | Icon transitions, abstract art |
| **DrawSVG** | SVG stroke drawing/erasing | Logo reveals, signatures, line art |
| **MotionPath** | Animate along SVG/custom paths | Orbital motion, path-following |
| **ScrambleText** | Character scramble decode | Tech intros, decode effects (use `--concurrency=1`) |
| **CustomEase** | Arbitrary easing from SVG paths | Brand-specific motion feel |
| **CustomBounce** | Custom bounce physics | Impact/landing effects |
| **CustomWiggle** | Custom wiggle/shake | Vibration, attention effects |
| **EasePack** | RoughEase, SlowMo, ExpoScale | Organic feel, cinematic speed ramps |
| **Physics2D** | 2D velocity/gravity/friction | Particle bursts (use fixed params) |
| **Flip** | FLIP layout transitions | Scene rearrangements (careful setup) |

### Not Recommended (Remotion native is better)

| Plugin | Reason | Alternative |
|--------|--------|-------------|
| **TextPlugin** | Typewriter effect is trivial with `interpolate()` + `.slice()` | `text.slice(0, interpolate(frame, ...))` |

### Not Compatible (Interactive / Scroll-based)

| Plugin | Reason |
|--------|--------|
| **ScrollTrigger** | No scrolling in video |
| **ScrollSmoother** | No scrolling in video |
| **ScrollTo** | No scrolling in video |
| **Draggable** | Requires mouse/touch interaction |
| **Inertia** | Requires velocity tracking |
| **Observer** | Event-based gestures |

### Determinism Warnings

| Plugin | Issue | Mitigation |
|--------|-------|------------|
| **ScrambleText** | Internal random char selection | Acceptable visually; use `--concurrency=1` for exact reproducibility |
| **RoughEase** | Internal randomness in jitter | Use fixed `taper` and `points`; acceptable for most use cases |
| **stagger: "random"** | GSAP's unseed random | Use function-based stagger with `seededRandom()` |

---

## Plugin Usage Patterns

### SplitText

```tsx
// Requires useGSAPWithFonts (waits for font loading)
const split = SplitText.create(element, {
  type: 'chars,words,lines',  // what to split into
  mask: 'lines',              // clip mask for reveal effect
  autoSplit: false,           // disable (Remotion has fixed dimensions)
});

// Access split elements
split.chars   // individual characters
split.words   // individual words
split.lines   // individual lines
```

| Config | Purpose |
|--------|---------|
| `type: "chars"` | Split into individual characters |
| `type: "words"` | Split into words |
| `type: "lines"` | Split into lines (based on line wrapping) |
| `type: "chars,words,lines"` | Split into all levels |
| `mask: "lines"` | Add overflow:hidden wrapper per line (for y-reveal) |
| `mask: "words"` | Add overflow:hidden wrapper per word |
| `mask: "chars"` | Add overflow:hidden wrapper per char |

### MorphSVG

```tsx
// Basic morph
tl.to('#path', { morphSVG: '#target-path', duration: 1.5 });

// With configuration
tl.to('#path', {
  morphSVG: {
    shape: '#target-path',    // target path selector or data
    type: 'rotational',       // "linear" or "rotational"
    map: 'size',              // "size", "position", "complexity"
    shapeIndex: 5,            // point alignment offset
    origin: '50% 50%',        // rotation origin
  },
  duration: 1.5, ease: 'power2.inOut',
});

// Convert shapes to paths first
MorphSVGPlugin.convertToPath('circle, rect, ellipse, polygon');
```

### DrawSVG

```tsx
// Draw from nothing to full
tl.from('.path', { drawSVG: 0, duration: 2 });

// Draw from center outward
tl.from('.path', { drawSVG: '50% 50%', duration: 2 });

// Animate to show only a segment
tl.to('.path', { drawSVG: '20% 80%', duration: 1 });

// Erase (draw to nothing)
tl.to('.path', { drawSVG: '100% 100%', duration: 1 });
```

### MotionPath

```tsx
tl.to('.element', {
  motionPath: {
    path: '#svg-path',        // SVG path to follow
    align: '#svg-path',       // align element center to path
    alignOrigin: [0.5, 0.5],  // center of element
    autoRotate: true,          // rotate to match path direction
    start: 0,                  // start position (0-1)
    end: 1,                    // end position (0-1)
  },
  duration: 3, ease: 'power1.inOut',
});

// Custom coordinate path (no SVG needed)
tl.to('.element', {
  motionPath: [
    { x: 100, y: 0 },
    { x: 200, y: -100 },
    { x: 300, y: 0 },
  ],
  duration: 2,
});
```

### CustomEase

```tsx
// Create from SVG path data
CustomEase.create('myEase', 'M0,0 C0.1,0.5 0.2,1 0.4,1 0.6,1 0.8,0.8 1,1');
tl.to(el, { y: -200, ease: 'myEase' });

// CustomBounce
CustomBounce.create('myBounce', {
  strength: 0.6,
  squash: 3,
  squashID: 'myBounce-squash',
});

// CustomWiggle
CustomWiggle.create('myWiggle', {
  wiggles: 8,
  type: 'easeOut',  // "easeOut", "easeInOut", "anticipate", "uniform", "random"
});
```

### ScrambleText

```tsx
tl.to('.element', {
  duration: 2,
  scrambleText: {
    text: 'FINAL TEXT',
    chars: '01',          // "upperCase", "lowerCase", "01", or custom string
    revealDelay: 0.5,
    speed: 0.3,           // 0-1
    newClass: 'revealed',
    oldClass: 'scrambled',
  },
});
```

### Physics2D (Particle Systems)

```tsx
// Use deterministic params (no random)
particles.forEach((p, i) => {
  const angle = (360 / count) * i;     // evenly distributed
  const velocity = 200 + (i % 5) * 40; // pattern-based, not random

  tl.to(p, {
    physics2D: { velocity, angle, gravity: 300 },
    opacity: 0, duration: 2,
  }, 0);
});
```

---

## Plugin Tiers

**Tier 1 -- Essential:**
- `gsap.timeline()` (core orchestration)
- `SplitText` (primary differentiator vs Remotion native)
- `CustomEase` / `EasePack` (motion feel beyond Remotion's `Easing`)

**Tier 2 -- Highly Useful:**
- `DrawSVG` (logo/line reveals -- impossible without GSAP)
- `MorphSVG` (shape morphing -- impossible without GSAP)
- `MotionPath` (path-following)
- `ScrambleText` (decode effects -- use `--concurrency=1`)

**Tier 3 -- Specialized:**
- `Physics2D` / `PhysicsProps` (particle systems)
- `CustomBounce` / `CustomWiggle` (bouncing/shaking)
- `Flip` (layout transitions)

### Note: 3D CSS Transforms

3D transforms (`rotateY`, `rotateX`, `perspective`, `preserve-3d`, `backfaceVisibility`) are **core GSAP features**, not plugins. No additional imports needed -- just use them in any `tl.to()` / `tl.from()` call.
