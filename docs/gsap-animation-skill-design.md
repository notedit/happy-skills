# GSAP Animation Skill - Architecture Design

> GSAP + Remotion integration for professional motion graphics video production

## 1. Overview

The `gsap-animation` skill provides a curated catalog of GSAP-powered motion graphics patterns, integrated with Remotion for deterministic video rendering. It complements the existing `react-animation` skill by offering GSAP's superior timeline orchestration, text splitting, SVG morphing, and advanced easing capabilities.

### Why GSAP + Remotion?

| Capability | Remotion Native | GSAP + Remotion |
|-----------|----------------|-----------------|
| Timeline orchestration | Manual with `<Sequence>` | `gsap.timeline()` with nesting, labels, position params |
| Easing | `Easing.*` (limited) | 50+ eases + CustomEase, RoughEase, CustomBounce, CustomWiggle |
| Text animation | Manual char splitting | SplitText (chars/words/lines with masks) |
| SVG morphing | Not built-in | MorphSVG (any shape to any shape) |
| SVG drawing | Not built-in | DrawSVG (stroke animation) |
| Path following | Not built-in | MotionPath (path-following with autoRotate) |
| Stagger | Manual loop + offset | Built-in stagger with grid, from, ease options |
| Reusable effects | Custom components | `gsap.registerEffect()` for named, parameterized effects |

### GSAP Licensing

All GSAP plugins are **100% free** since Webflow's acquisition in 2024, including former Club plugins (SplitText, MorphSVG, DrawSVG, MotionPath, etc.).

---

## 2. Core Integration: useGSAPTimeline Hook

The central bridge between GSAP and Remotion. GSAP timelines are created, paused, and seeked to match Remotion's frame-based rendering.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';
import gsap from 'gsap';
import { useEffect, useRef, useCallback } from 'react';

/**
 * Sync a GSAP timeline with Remotion's frame-based rendering.
 *
 * - Creates the timeline once (paused)
 * - Seeks to the correct position on every frame
 * - Cleans up on unmount
 */
function useGSAPTimeline(
  factory: (tl: gsap.core.Timeline) => void,
  deps: any[] = []
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tlRef = useRef<gsap.core.Timeline | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Create timeline once
  useEffect(() => {
    if (!containerRef.current) return;

    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ paused: true });
      factory(tl);
      tlRef.current = tl;
    }, containerRef);

    return () => {
      ctx.revert(); // Clean up all GSAP animations
      tlRef.current = null;
    };
  }, deps);

  // Seek to current frame position
  useEffect(() => {
    if (tlRef.current) {
      tlRef.current.seek(frame / fps);
    }
  }, [frame, fps]);

  return containerRef;
}
```

**Key Design Decisions:**
- `gsap.context()` scopes all animations to a container, enabling clean teardown
- `tl.pause()` prevents auto-play; `tl.seek()` gives Remotion full time control
- Timeline is created once; only `seek()` runs per frame (performance)
- `deps` array allows timeline recreation when dynamic props change

---

## 3. Plugin Integration Matrix

### Compatible Plugins (Remotion-safe)

| Plugin | Status | Notes |
|--------|--------|-------|
| **SplitText** | Full | Chars/words/lines splitting + mask reveals |
| **MorphSVG** | Full | Shape-to-shape morphing |
| **DrawSVG** | Full | Stroke drawing/erasing |
| **MotionPath** | Full | Path-following with autoRotate |
| **ScrambleText** | Full | Character scramble decode effect |
| **TextPlugin** | Full | Character-by-character typewriter |
| **CustomEase** | Full | Arbitrary easing curves |
| **EasePack** | Full | RoughEase, SlowMo, ExpoScale |
| **CustomBounce** | Full | Custom bounce physics |
| **CustomWiggle** | Full | Custom shake/wiggle |
| **Flip** | Partial | Works if DOM changes are frame-deterministic |
| **Physics2D** | Partial | Non-deterministic; needs seeded random workaround |

### Incompatible Plugins (No video use case)

| Plugin | Reason |
|--------|--------|
| ScrollTrigger | Scroll-driven, no scroll in video |
| Draggable | User interaction required |
| Observer | Event-driven |
| Inertia | Velocity-tracking, interactive |
| ScrollSmoother | Scroll-driven |
| ScrollTo | Scroll-driven |

---

## 4. Animation Categories & Patterns

### Category 1: Text Animations

**SplitText Reveal** - Char/word/line animations with mask clipping
```tsx
const GSAPTextReveal: React.FC<{
  text: string;
  splitType?: 'chars' | 'words' | 'lines';
  stagger?: number;
  duration?: number;
  startAt?: number; // seconds
}> = ({ text, splitType = 'chars', stagger = 0.03, duration = 0.6, startAt = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);

  const ref = useGSAPTimeline((tl) => {
    const split = SplitText.create(containerRef.current!, {
      type: splitType,
      mask: splitType,
    });
    tl.from(split[splitType === 'chars' ? 'chars' : splitType === 'words' ? 'words' : 'lines'], {
      y: '100%',
      duration,
      stagger,
      ease: 'power3.out',
    }, startAt);
  });

  return <div ref={ref}><div ref={containerRef}>{text}</div></div>;
};
```

**ScrambleText** - Decode/encrypt character effect
**TextPlugin Typewriter** - Character-by-character typing
**Kinetic Typography** - Multi-word dramatic entrances with scale, rotation

### Category 2: SVG Animations

**MorphSVG** - Shape-to-shape morphing
**DrawSVG** - Logo reveals, signature drawing, line art
**MotionPath** - Elements following SVG paths with autoRotate

### Category 3: Transition Effects

**Clip-Path Transitions** - Circle reveal, diagonal wipe, iris, blinds
**Slide/Push** - Directional scene transitions
**Zoom/Scale** - Scale-based transitions
**Crossfade** - Opacity crossfade between scenes

### Category 4: Motion Graphics Templates

**Lower Thirds** - Name/title overlay with bar + text reveal
**Title Cards** - Intro sequences with split text + decorative elements
**Logo Reveals** - DrawSVG stroke → fill, scale + rotation, morph from abstract
**Data Visualization** - Counter animation, bar charts, donut charts
**CTA Overlays** - Call-to-action with pulse attention
**End Screens** - Outro with social icons + subscribe

### Category 5: Advanced Effects

**Particle Systems** - Physics2D-driven particle bursts (seeded for determinism)
**3D Transforms** - Perspective-based card flips, text rotations
**Color/Gradient Transitions** - Animated gradients via custom property tweening

---

## 5. Skill Structure

```
skills/gsap-animation/
├── SKILL.md                          # Main skill doc (pattern catalog + usage guide)
├── rules/
│   ├── remotion-integration.md       # useGSAPTimeline hook + Remotion patterns
│   ├── plugin-guide.md               # GSAP plugin compatibility + usage in Remotion
│   └── timing-conventions.md         # Standard timing/easing for motion graphics
```

---

## 6. SKILL.md Design

The SKILL.md should be organized as:

1. **When to Use** - GSAP vs Remotion native `interpolate()`
2. **Setup** - Install GSAP + register plugins in Remotion project
3. **Core Hook** - `useGSAPTimeline` pattern
4. **Animation Catalog** by category:
   - Text Animations (SplitText, ScrambleText, TextPlugin, Kinetic)
   - SVG Animations (MorphSVG, DrawSVG, MotionPath)
   - Transitions (clip-path, slide, zoom, crossfade)
   - Templates (lower third, title card, logo reveal, counter, CTA, end screen)
5. **Easing Reference** - GSAP ease → motion graphics use case mapping
6. **Registered Effects** - Pre-built `gsap.registerEffect()` library
7. **Style Consistency** - Do/Don't guidelines
8. **Project Setup** - Remotion + GSAP project scaffolding

---

## 7. When to Use GSAP vs Remotion Native

| Scenario | Use | Why |
|----------|-----|-----|
| Simple fade/slide entrance | Remotion `interpolate()` | Simpler, no GSAP overhead |
| Single property animation | Remotion `interpolate()` | Direct and clear |
| Spring physics | Remotion `spring()` | Purpose-built |
| Complex multi-step sequence | **GSAP timeline** | Nesting, labels, position params |
| Staggered animation across 10+ elements | **GSAP stagger** | Built-in grid, from, ease |
| Text char/word/line split | **GSAP SplitText** | No Remotion equivalent |
| SVG shape morphing | **GSAP MorphSVG** | No Remotion equivalent |
| SVG stroke drawing | **GSAP DrawSVG** | No Remotion equivalent |
| Path-following animation | **GSAP MotionPath** | No Remotion equivalent |
| Custom easing curve | **GSAP CustomEase** | SVG path-based curves |
| Character scramble effect | **GSAP ScrambleText** | No Remotion equivalent |
| Reusable named effects | **GSAP registerEffect** | Fluent timeline API extension |

---

## 8. Relationship to react-animation Skill

| Aspect | react-animation | gsap-animation |
|--------|----------------|----------------|
| **Focus** | ReactBits visual components (shaders, WebGL backgrounds) | GSAP timeline-based motion graphics |
| **Animation engine** | Remotion `interpolate()` + CSS/WebGL | GSAP timeline + plugins |
| **Best for** | Visual effects, backgrounds, atmospherics | Text animation, SVG, transitions, templates |
| **Components** | 35 curated visual components | Animation patterns + templates |
| **Integration** | Frame-driven via `useCurrentFrame()` | Frame-driven via `useGSAPTimeline()` |

**Complementary Usage:**
```tsx
// Combine both skills in one Remotion composition
const Scene: React.FC = () => (
  <AbsoluteFill>
    {/* react-animation: background atmosphere */}
    <Aurora colorStops={['#3A29FF', '#FF94B4']} />

    {/* gsap-animation: text + SVG motion graphics */}
    <GSAPTextReveal text="Beautiful Motion" splitType="chars" />
    <GSAPLogoReveal svgPath={logoSVG} />

    {/* react-animation: film grain overlay */}
    <NoiseOverlay opacity={0.05} />
  </AbsoluteFill>
);
```

---

## 9. Project Setup Template

```bash
# New Remotion + GSAP project
npx create-video@latest my-motion-graphics
cd my-motion-graphics

# Install GSAP (all plugins now free)
npm install gsap

# Register plugins in src/Root.tsx
```

```tsx
// src/gsap-setup.ts
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin';
import { MotionPathPlugin } from 'gsap/MotionPathPlugin';
import { ScrambleTextPlugin } from 'gsap/ScrambleTextPlugin';
import { TextPlugin } from 'gsap/TextPlugin';
import { CustomEase } from 'gsap/CustomEase';
import { CustomBounce } from 'gsap/CustomBounce';
import { CustomWiggle } from 'gsap/CustomWiggle';

gsap.registerPlugin(
  SplitText,
  MorphSVGPlugin,
  DrawSVGPlugin,
  MotionPathPlugin,
  ScrambleTextPlugin,
  TextPlugin,
  CustomEase,
  CustomBounce,
  CustomWiggle,
);

export { gsap };
```

---

## 10. Registered Effects Library

Pre-built effects that extend the timeline API:

```tsx
// effects/text.ts
gsap.registerEffect({
  name: 'textReveal',
  effect: (targets, config) => {
    const split = SplitText.create(targets, { type: config.type, mask: config.type });
    return gsap.from(split[config.type], {
      y: '100%', duration: config.duration, stagger: config.stagger, ease: config.ease,
    });
  },
  defaults: { type: 'lines', duration: 0.6, stagger: 0.15, ease: 'power3.out' },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'charCascade',
  effect: (targets, config) => {
    const split = SplitText.create(targets, { type: 'chars' });
    return gsap.from(split.chars, {
      y: 50, opacity: 0, rotationX: -90, duration: config.duration,
      stagger: config.stagger, ease: config.ease,
    });
  },
  defaults: { duration: 0.5, stagger: 0.02, ease: 'back.out(1.7)' },
  extendTimeline: true,
});

// effects/transitions.ts
gsap.registerEffect({
  name: 'circleReveal',
  effect: (targets, config) => gsap.fromTo(targets,
    { clipPath: 'circle(0% at 50% 50%)' },
    { clipPath: `circle(${config.radius} at ${config.cx} ${config.cy})`, duration: config.duration, ease: config.ease },
  ),
  defaults: { radius: '75%', cx: '50%', cy: '50%', duration: 1, ease: 'power2.out' },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'wipeIn',
  effect: (targets, config) => gsap.fromTo(targets,
    { clipPath: 'inset(0 100% 0 0)' },
    { clipPath: 'inset(0 0% 0 0)', duration: config.duration, ease: config.ease },
  ),
  defaults: { duration: 0.8, ease: 'power2.inOut' },
  extendTimeline: true,
});

// effects/svg.ts
gsap.registerEffect({
  name: 'drawIn',
  effect: (targets, config) => gsap.from(targets, {
    drawSVG: 0, duration: config.duration, ease: config.ease, stagger: config.stagger,
  }),
  defaults: { duration: 1.5, ease: 'power2.inOut', stagger: 0.1 },
  extendTimeline: true,
});

gsap.registerEffect({
  name: 'morphTo',
  effect: (targets, config) => gsap.to(targets, {
    morphSVG: config.shape, duration: config.duration, ease: config.ease,
  }),
  defaults: { duration: 1.5, ease: 'power2.inOut' },
  extendTimeline: true,
});
```

**Usage in timeline:**
```tsx
const ref = useGSAPTimeline((tl) => {
  tl.textReveal('.title')
    .charCascade('.subtitle', {}, '-=0.3')
    .circleReveal('.scene-2', {}, '+=0.5')
    .drawIn('.logo-path')
    .morphTo('.icon', { shape: '#target-shape' });
});
```

---

## 11. Timing Conventions

| Element | Duration | Ease | Notes |
|---------|----------|------|-------|
| Text entrance (per line) | 0.5-0.8s | `power2.out` / `power3.out` | |
| Text entrance (per char stagger) | 0.02-0.05s | - | Gap between chars |
| Text entrance (per word stagger) | 0.08-0.15s | - | Gap between words |
| Text exit | 0.3-0.5s | `power2.in` | Faster than entrance |
| Scene transition | 0.5-1.0s | `power2.inOut` | |
| Logo reveal (DrawSVG) | 1.5-2.5s | `power2.inOut` | Slow, deliberate |
| Shape morph | 1.0-2.0s | `power2.inOut` | Smooth, cinematic |
| Lower third total | 4-6s | - | In + hold + out |
| Hold for readable text | 2-4s | - | Depends on word count |
| Counter animation | 1.5-3.0s | `power1.out` | |
| Dramatic entrance | 0.5-1.0s | `expo.out` / `back.out(1.7)` | |
| Attention pulse | 0.3-0.5s | `sine.inOut` | Repeat, yoyo |

---

## 12. Easing Quick Reference

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
| Custom curve | `CustomEase` | Brand-specific motion |
