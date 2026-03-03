---
name: spring-animation
description: Remotion spring physics for motion graphics video production. Bouncy entrances, elastic trails, orchestrated sequences, physics presets, and organic motion patterns that interpolate() alone cannot achieve.
metadata:
  tags: spring, remotion, motion-graphics, animation, video, physics, bounce, elastic, trail, stagger
---

## When to use

Use this skill when creating Remotion video compositions that need **spring physics** -- natural, organic motion with bounce, overshoot, and elastic settling.

**Use spring when you need:**
- Bouncy/elastic entrances (overshoot + settle)
- Organic deceleration (not linear, not eased -- physically modeled)
- Staggered trails with spring physics per element
- Number counters that overshoot then settle
- Scale/rotate with natural weight and inertia
- Enter + exit animations with spring math (`in - out`)
- Multi-property orchestration with different spring configs per property

**Use Remotion native `interpolate()` when:**
- Linear or eased motion with no bounce (fade, slide, wipe)
- Exact timing control (must end at precisely frame N)
- Clip-path animations
- Progress bars / deterministic counters

**Use GSAP (gsap-animation skill) when:**
- Text splitting (SplitText: chars/words/lines with mask)
- SVG stroke drawing (DrawSVG)
- SVG morphing (MorphSVG)
- Complex timeline orchestration with labels and position parameters
- ScrambleText decode effects
- Registered reusable effects

**Note:** `@react-spring/web` is NOT compatible with Remotion (it uses requestAnimationFrame internally). This skill uses Remotion's native `spring()` function which provides the same physics model in a frame-deterministic way.

---

## Core API

### spring()

Returns a value from 0 to 1 (can overshoot past 1 with low damping) based on spring physics simulation.

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const value = spring({
  frame,
  fps,
  config: {
    damping: 10,     // 1-200: higher = less bounce
    stiffness: 100,  // 1-200: higher = faster snap
    mass: 1,         // 0.1-5: higher = more inertia
  },
});
```

### Config Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `damping` | 1-200 | 10 | Resistance. Low = bouncy, high = smooth |
| `stiffness` | 1-200 | 100 | Snap speed. High = fast, low = slow |
| `mass` | 0.1-5 | 1 | Weight/inertia. High = sluggish, low = light |
| `overshootClamping` | bool | false | Clamp at target (no overshoot) |

### Additional Options

| Option | Type | Effect |
|--------|------|--------|
| `delay` | number | Delay start by N frames (returns 0 until delay elapses) |
| `durationInFrames` | number | Force spring to settle within N frames |
| `reverse` | bool | Animate from 1 to 0 |
| `from` | number | Starting value (default 0) |
| `to` | number | Ending value (default 1) |

### measureSpring()

Calculate how many frames a spring config takes to settle. Essential for `<Sequence>` and composition duration.

```tsx
import { measureSpring } from 'remotion';

const frames = measureSpring({
  fps: 30,
  config: { damping: 10, stiffness: 100 },
}); // => number of frames until settled
```

---

## Physics Presets

```tsx
// src/spring-presets.ts
import { SpringConfig } from 'remotion';

export const SPRING = {
  // Smooth, no bounce -- subtle reveals, background motion
  smooth: { damping: 200 } as Partial<SpringConfig>,

  // Snappy, minimal bounce -- UI elements, clean entrances
  snappy: { damping: 20, stiffness: 200 } as Partial<SpringConfig>,

  // Bouncy -- playful entrances, attention-grabbing
  bouncy: { damping: 8 } as Partial<SpringConfig>,

  // Heavy, slow -- dramatic reveals, weighty objects
  heavy: { damping: 15, stiffness: 80, mass: 2 } as Partial<SpringConfig>,

  // Wobbly -- elastic, cartoon-like overshoot
  wobbly: { damping: 4, stiffness: 80 } as Partial<SpringConfig>,

  // Stiff -- fast snap with tiny bounce
  stiff: { damping: 15, stiffness: 300 } as Partial<SpringConfig>,

  // Gentle -- slow, dreamy, organic
  gentle: { damping: 20, stiffness: 40, mass: 1.5 } as Partial<SpringConfig>,

  // Molasses -- very slow, heavy, barely bounces
  molasses: { damping: 25, stiffness: 30, mass: 3 } as Partial<SpringConfig>,

  // Pop -- strong overshoot for scale-in effects
  pop: { damping: 6, stiffness: 150 } as Partial<SpringConfig>,

  // Rubber -- exaggerated elastic bounce
  rubber: { damping: 3, stiffness: 100, mass: 0.5 } as Partial<SpringConfig>,
} as const;
```

### Preset Visual Reference

| Preset | Bounce | Speed | Feel | Best For |
|--------|--------|-------|------|----------|
| `smooth` | None | Medium | Butter | Background, subtle reveals |
| `snappy` | Minimal | Fast | Crisp | UI elements, buttons |
| `bouncy` | Strong | Medium | Playful | Titles, icons, attention |
| `heavy` | Small | Slow | Weighty | Dramatic reveals, large objects |
| `wobbly` | Extreme | Medium | Cartoon | Playful, humorous |
| `stiff` | Tiny | Very fast | Mechanical | Data viz, precise motion |
| `gentle` | Minimal | Slow | Dreamy | Luxury, calm, organic |
| `molasses` | Almost none | Very slow | Heavy | Cinematic, suspense |
| `pop` | Strong | Fast | Punchy | Scale-in, badge, icon pop |
| `rubber` | Extreme | Fast | Elastic | Exaggerated, cartoon, fun |

---

## 1. Spring Entrance Patterns

### Basic Spring Entrance

```tsx
import { spring, interpolate, useCurrentFrame, useVideoConfig, AbsoluteFill } from 'remotion';
import { SPRING } from './spring-presets';

const SpringEntrance: React.FC<{
  children: React.ReactNode;
  preset?: keyof typeof SPRING;
  delay?: number;
}> = ({ children, preset = 'bouncy', delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, delay, config: SPRING[preset] });
  const translateY = interpolate(progress, [0, 1], [60, 0]);

  return (
    <AbsoluteFill style={{
      opacity: progress,
      transform: `translateY(${translateY}px)`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
```

### Scale Pop

```tsx
const ScalePop: React.FC<{
  children: React.ReactNode;
  delay?: number;
}> = ({ children, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // pop preset overshoots past 1, creating natural scale bounce
  const scale = spring({ frame, fps, delay, config: SPRING.pop });
  const opacity = spring({ frame, fps, delay, config: SPRING.smooth });

  return (
    <div style={{
      transform: `scale(${scale})`,
      opacity,
    }}>
      {children}
    </div>
  );
};
```

### Enter + Exit (Spring Math)

```tsx
const EnterExit: React.FC<{
  children: React.ReactNode;
  enterDelay?: number;
  exitBeforeEnd?: number; // frames before composition end to start exit
}> = ({ children, enterDelay = 0, exitBeforeEnd = 30 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const enter = spring({ frame, fps, delay: enterDelay, config: SPRING.bouncy });
  const exit = spring({
    frame, fps,
    delay: durationInFrames - exitBeforeEnd,
    config: SPRING.snappy,
  });

  const scale = enter - exit; // 0 -> 1 -> 0
  const opacity = enter - exit;

  return (
    <div style={{ transform: `scale(${scale})`, opacity }}>
      {children}
    </div>
  );
};
```

---

## 2. Trail / Stagger Patterns

### Spring Trail (staggered entrance)

Mimics React Spring's `useTrail` -- each element enters with a frame delay.

```tsx
const SpringTrail: React.FC<{
  items: React.ReactNode[];
  staggerFrames?: number;
  preset?: keyof typeof SPRING;
  direction?: 'up' | 'down' | 'left' | 'right';
}> = ({ items, staggerFrames = 4, preset = 'bouncy', direction = 'up' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const getOffset = (progress: number) => {
    const distance = 50;
    const remaining = interpolate(progress, [0, 1], [distance, 0]);
    switch (direction) {
      case 'up': return { transform: `translateY(${remaining}px)` };
      case 'down': return { transform: `translateY(${-remaining}px)` };
      case 'left': return { transform: `translateX(${remaining}px)` };
      case 'right': return { transform: `translateX(${-remaining}px)` };
    }
  };

  return (
    <>
      {items.map((item, i) => {
        const delay = i * staggerFrames;
        const progress = spring({ frame, fps, delay, config: SPRING[preset] });
        return (
          <div key={i} style={{ opacity: progress, ...getOffset(progress) }}>
            {item}
          </div>
        );
      })}
    </>
  );
};
```

### Character Trail (text animation)

Manual character splitting with spring stagger. For advanced text splitting (mask reveals, line wrapping), use gsap-animation skill instead.

```tsx
const CharacterTrail: React.FC<{
  text: string;
  staggerFrames?: number;
  preset?: keyof typeof SPRING;
  fontSize?: number;
}> = ({ text, staggerFrames = 2, preset = 'pop', fontSize = 80 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: 'flex', justifyContent: 'center', overflow: 'hidden' }}>
      {text.split('').map((char, i) => {
        const delay = i * staggerFrames;
        const progress = spring({ frame, fps, delay, config: SPRING[preset] });
        const translateY = interpolate(progress, [0, 1], [fontSize, 0]);

        return (
          <span key={i} style={{
            display: 'inline-block',
            fontSize,
            fontWeight: 'bold',
            color: '#fff',
            opacity: progress,
            transform: `translateY(${translateY}px)`,
            whiteSpace: 'pre',
          }}>
            {char === ' ' ? '\u00A0' : char}
          </span>
        );
      })}
    </div>
  );
};
```

### Word Trail

```tsx
const WordTrail: React.FC<{
  text: string;
  staggerFrames?: number;
  preset?: keyof typeof SPRING;
  fontSize?: number;
}> = ({ text, staggerFrames = 5, preset = 'bouncy', fontSize = 64 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(' ');

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3em', justifyContent: 'center' }}>
      {words.map((word, i) => {
        const delay = i * staggerFrames;
        const progress = spring({ frame, fps, delay, config: SPRING[preset] });
        const scale = spring({ frame, fps, delay, config: SPRING.pop });

        return (
          <span key={i} style={{
            display: 'inline-block',
            fontSize,
            fontWeight: 'bold',
            color: '#fff',
            opacity: progress,
            transform: `scale(${scale})`,
          }}>
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

### Grid Stagger (center-out)

```tsx
const GridStagger: React.FC<{
  items: React.ReactNode[];
  columns: number;
  cellSize?: number;
  gap?: number;
}> = ({ items, columns, cellSize = 120, gap = 16 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rows = Math.ceil(items.length / columns);
  const centerCol = (columns - 1) / 2;
  const centerRow = (rows - 1) / 2;

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: `repeat(${columns}, ${cellSize}px)`,
      gap,
    }}>
      {items.map((item, i) => {
        const col = i % columns;
        const row = Math.floor(i / columns);
        // Distance from center determines delay
        const dist = Math.sqrt((col - centerCol) ** 2 + (row - centerRow) ** 2);
        const delay = Math.round(dist * 4);
        const progress = spring({ frame, fps, delay, config: SPRING.pop });

        return (
          <div key={i} style={{
            width: cellSize, height: cellSize,
            opacity: progress,
            transform: `scale(${progress})`,
          }}>
            {item}
          </div>
        );
      })}
    </div>
  );
};
```

---

## 3. Chain / Sequence Patterns

### Spring Chain (sequential animations)

Mimics React Spring's `useChain` -- animations trigger in sequence using `measureSpring` for timing.

```tsx
import { spring, measureSpring, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

const SpringChain: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Step 1: Container scales in
  const step1Config = SPRING.bouncy;
  const step1 = spring({ frame, fps, config: step1Config });
  const step1Duration = measureSpring({ fps, config: step1Config });

  // Step 2: Title fades up (starts when step1 is 80% done)
  const step2Delay = Math.round(step1Duration * 0.8);
  const step2Config = SPRING.snappy;
  const step2 = spring({ frame, fps, delay: step2Delay, config: step2Config });
  const step2Duration = measureSpring({ fps, config: step2Config });

  // Step 3: Subtitle appears (starts when step2 finishes)
  const step3Delay = step2Delay + step2Duration;
  const step3 = spring({ frame, fps, delay: step3Delay, config: SPRING.gentle });

  return (
    <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      {/* Container */}
      <div style={{
        transform: `scale(${step1})`,
        opacity: step1,
        background: '#1e293b',
        padding: 60,
        borderRadius: 24,
        textAlign: 'center',
      }}>
        {/* Title */}
        <h1 style={{
          fontSize: 72, fontWeight: 'bold', color: '#fff',
          opacity: step2,
          transform: `translateY(${interpolate(step2, [0, 1], [30, 0])}px)`,
        }}>Spring Chain</h1>
        {/* Subtitle */}
        <p style={{
          fontSize: 28, color: 'rgba(255,255,255,0.7)', marginTop: 16,
          opacity: step3,
          transform: `translateY(${interpolate(step3, [0, 1], [20, 0])}px)`,
        }}>Sequential spring orchestration</p>
      </div>
    </AbsoluteFill>
  );
};
```

### useSpringChain Hook

Reusable hook for chaining multiple springs with overlap control.

```tsx
import { spring, measureSpring, SpringConfig, useCurrentFrame, useVideoConfig } from 'remotion';

type ChainStep = {
  config: Partial<SpringConfig>;
  overlap?: number; // 0-1, how much to overlap with previous step (default 0)
};

function useSpringChain(steps: ChainStep[]) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  let currentDelay = 0;
  return steps.map((step, i) => {
    if (i > 0) {
      const prevDuration = measureSpring({ fps, config: steps[i - 1].config });
      const overlap = step.overlap ?? 0;
      currentDelay += Math.round(prevDuration * (1 - overlap));
    }
    return spring({ frame, fps, delay: currentDelay, config: step.config });
  });
}

// Usage:
const [container, title, subtitle, cta] = useSpringChain([
  { config: SPRING.bouncy },
  { config: SPRING.snappy, overlap: 0.2 },
  { config: SPRING.gentle, overlap: 0.3 },
  { config: SPRING.pop, overlap: 0.1 },
]);
```

---

## 4. Multi-Property Springs

### Different physics per property

```tsx
const MultiPropertySpring: React.FC<{ delay?: number }> = ({ delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Position: snappy (arrives fast)
  const position = spring({ frame, fps, delay, config: SPRING.snappy });
  // Scale: bouncy (overshoots then settles)
  const scale = spring({ frame, fps, delay, config: SPRING.bouncy });
  // Rotation: wobbly (elastic wobble)
  const rotation = spring({ frame, fps, delay, config: SPRING.wobbly });
  // Opacity: smooth (no bounce)
  const opacity = spring({ frame, fps, delay, config: SPRING.smooth });

  const translateX = interpolate(position, [0, 1], [-300, 0]);
  const rotate = interpolate(rotation, [0, 1], [-15, 0]);

  return (
    <div style={{
      transform: `translateX(${translateX}px) scale(${scale}) rotate(${rotate}deg)`,
      opacity,
    }}>
      Multi-Property
    </div>
  );
};
```

---

## 5. Spring Counter

Number counter with spring physics -- overshoots the target then settles.

```tsx
const SpringCounter: React.FC<{
  endValue: number;
  prefix?: string;
  suffix?: string;
  preset?: keyof typeof SPRING;
  delay?: number;
}> = ({ endValue, prefix = '', suffix = '', preset = 'bouncy', delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, delay, config: SPRING[preset] });
  // With bouncy config, progress overshoots past 1.0 before settling
  // This means the counter briefly shows a number > endValue, then settles
  const value = Math.round(progress * endValue);

  return (
    <div style={{
      fontSize: 96, fontWeight: 'bold', color: '#fff',
      fontVariantNumeric: 'tabular-nums',
    }}>
      {prefix}{value.toLocaleString()}{suffix}
    </div>
  );
};
```

**Comparison with linear counter:**
- `interpolate()` counter: smoothly reaches exact target, no overshoot
- Spring counter: overshoots then settles -- feels more energetic and alive

---

## 6. 3D Transform Patterns

### Spring Card Flip

```tsx
const SpringCardFlip: React.FC<{
  frontContent: React.ReactNode;
  backContent: React.ReactNode;
  flipDelay?: number;
}> = ({ frontContent, backContent, flipDelay = 15 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const flipProgress = spring({
    frame, fps, delay: flipDelay,
    config: { damping: 15, stiffness: 80 }, // slow, weighty flip
  });
  const rotateY = interpolate(flipProgress, [0, 1], [0, 180]);

  return (
    <AbsoluteFill style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ perspective: 800 }}>
        <div style={{
          width: 500, height: 320, position: 'relative',
          transformStyle: 'preserve-3d',
          transform: `rotateY(${rotateY}deg)`,
        }}>
          <div style={{
            position: 'absolute', inset: 0, backfaceVisibility: 'hidden',
            background: '#1e293b', borderRadius: 16,
            display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 32,
          }}>{frontContent}</div>
          <div style={{
            position: 'absolute', inset: 0, backfaceVisibility: 'hidden',
            background: '#3b82f6', borderRadius: 16, transform: 'rotateY(180deg)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 32,
          }}>{backContent}</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### Perspective Tilt

```tsx
const PerspectiveTilt: React.FC<{
  children: React.ReactNode;
  rotateX?: number;
  rotateY?: number;
  delay?: number;
}> = ({ children, rotateX = -20, rotateY = 15, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, delay, config: SPRING.heavy });
  const rx = interpolate(progress, [0, 1], [rotateX, 0]);
  const ry = interpolate(progress, [0, 1], [rotateY, 0]);
  const translateZ = interpolate(progress, [0, 1], [-200, 0]);

  return (
    <div style={{
      perspective: 1000,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <div style={{
        transform: `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) translateZ(${translateZ}px)`,
        opacity: progress,
      }}>
        {children}
      </div>
    </div>
  );
};
```

---

## 7. Spring Transitions

### Crossfade with Spring

```tsx
const SpringCrossfade: React.FC<{
  outgoing: React.ReactNode;
  incoming: React.ReactNode;
  switchFrame: number;
}> = ({ outgoing, incoming, switchFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const outOpacity = frame < switchFrame ? 1 : 1 - spring({
    frame: frame - switchFrame, fps, config: SPRING.smooth,
  });
  const inOpacity = frame < switchFrame ? 0 : spring({
    frame: frame - switchFrame, fps, config: SPRING.smooth,
  });
  const inScale = frame < switchFrame ? 0.95 : interpolate(
    spring({ frame: frame - switchFrame, fps, config: SPRING.bouncy }),
    [0, 1], [0.95, 1]
  );

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: outOpacity }}>{outgoing}</AbsoluteFill>
      <AbsoluteFill style={{ opacity: inOpacity, transform: `scale(${inScale})` }}>
        {incoming}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

### Slide Transition with Spring

```tsx
const SpringSlide: React.FC<{
  outgoing: React.ReactNode;
  incoming: React.ReactNode;
  switchFrame: number;
  direction?: 'left' | 'right' | 'up' | 'down';
}> = ({ outgoing, incoming, switchFrame, direction = 'left' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = frame < switchFrame ? 0 : spring({
    frame: frame - switchFrame, fps, config: SPRING.snappy,
  });

  const getTransform = (isOutgoing: boolean) => {
    const offset = isOutgoing ? interpolate(progress, [0, 1], [0, -100]) : interpolate(progress, [0, 1], [100, 0]);
    switch (direction) {
      case 'left': return `translateX(${offset}%)`;
      case 'right': return `translateX(${-offset}%)`;
      case 'up': return `translateY(${offset}%)`;
      case 'down': return `translateY(${-offset}%)`;
    }
  };

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: getTransform(true) }}>{outgoing}</AbsoluteFill>
      <AbsoluteFill style={{ transform: getTransform(false) }}>{incoming}</AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## 8. Templates

### Spring Title Card

```tsx
const SpringTitleCard: React.FC<{
  title: string;
  subtitle?: string;
  accent?: string;
}> = ({ title, subtitle, accent = '#3b82f6' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Background shape
  const bgScale = spring({ frame, fps, config: SPRING.heavy });
  // Title words stagger
  const words = title.split(' ');
  // Divider
  const dividerWidth = spring({ frame, fps, delay: 8, config: SPRING.snappy });
  // Subtitle
  const subtitleProgress = spring({ frame, fps, delay: 15, config: SPRING.gentle });

  return (
    <AbsoluteFill style={{
      background: '#0f172a',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      {/* Accent circle */}
      <div style={{
        position: 'absolute', width: 300, height: 300, borderRadius: '50%',
        background: `${accent}20`, transform: `scale(${bgScale})`,
      }} />

      <div style={{ textAlign: 'center', position: 'relative', zIndex: 1 }}>
        {/* Title with word stagger */}
        <div style={{ display: 'flex', gap: '0.3em', justifyContent: 'center', flexWrap: 'wrap' }}>
          {words.map((word, i) => {
            const delay = i * 4;
            const progress = spring({ frame, fps, delay, config: SPRING.pop });
            const y = interpolate(progress, [0, 1], [40, 0]);
            return (
              <span key={i} style={{
                fontSize: 80, fontWeight: 'bold', color: '#fff',
                display: 'inline-block',
                opacity: progress,
                transform: `translateY(${y}px) scale(${progress})`,
              }}>{word}</span>
            );
          })}
        </div>

        {/* Divider */}
        <div style={{
          width: 80, height: 3, background: accent, margin: '20px auto',
          transform: `scaleX(${dividerWidth})`, transformOrigin: 'center',
        }} />

        {/* Subtitle */}
        {subtitle && (
          <p style={{
            fontSize: 28, color: 'rgba(255,255,255,0.7)',
            opacity: subtitleProgress,
            transform: `translateY(${interpolate(subtitleProgress, [0, 1], [15, 0])}px)`,
          }}>{subtitle}</p>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

### Spring Lower Third

```tsx
const SpringLowerThird: React.FC<{
  name: string;
  title: string;
  accent?: string;
  hold?: number;
}> = ({ name, title, accent = '#3b82f6', hold = 90 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Enter
  const barIn = spring({ frame, fps, config: SPRING.snappy });
  const nameIn = spring({ frame, fps, delay: 6, config: SPRING.bouncy });
  const titleIn = spring({ frame, fps, delay: 10, config: SPRING.gentle });

  // Exit (spring math subtraction)
  const exitDelay = durationInFrames - 20;
  const barOut = spring({ frame, fps, delay: exitDelay, config: SPRING.stiff });
  const nameOut = spring({ frame, fps, delay: exitDelay - 4, config: SPRING.stiff });
  const titleOut = spring({ frame, fps, delay: exitDelay - 8, config: SPRING.stiff });

  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', bottom: 80, left: 60 }}>
        {/* Bar */}
        <div style={{
          background: accent, padding: '12px 24px', borderRadius: 4,
          transform: `scaleX(${barIn - barOut})`,
          transformOrigin: 'left',
          opacity: barIn - barOut,
        }}>
          <div style={{
            fontSize: 28, fontWeight: 'bold', color: '#fff',
            opacity: nameIn - nameOut,
            transform: `translateX(${interpolate(nameIn - nameOut, [0, 1], [-20, 0])}px)`,
          }}>{name}</div>
          <div style={{
            fontSize: 18, color: 'rgba(255,255,255,0.8)',
            opacity: titleIn - titleOut,
            transform: `translateX(${interpolate(titleIn - titleOut, [0, 1], [-15, 0])}px)`,
          }}>{title}</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### Spring Feature Grid

```tsx
const SpringFeatureGrid: React.FC<{
  features: Array<{ icon: string; label: string }>;
  columns?: number;
}> = ({ features, columns = 3 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#0f172a',
    }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 200px)`,
        gap: 32,
      }}>
        {features.map(({ icon, label }, i) => {
          const delay = i * 5;
          const scale = spring({ frame, fps, delay, config: SPRING.pop });
          const opacity = spring({ frame, fps, delay, config: SPRING.smooth });

          return (
            <div key={i} style={{
              textAlign: 'center', padding: 24,
              background: 'rgba(255,255,255,0.05)', borderRadius: 16,
              transform: `scale(${scale})`, opacity,
            }}>
              <div style={{ fontSize: 48 }}>{icon}</div>
              <div style={{ fontSize: 18, color: '#fff', marginTop: 12 }}>{label}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

### Spring Outro

```tsx
const SpringOutro: React.FC<{
  headline: string;
  tagline?: string;
  ctaText?: string;
  accent?: string;
}> = ({ headline, tagline, ctaText, accent = '#3b82f6' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headlineProgress = spring({ frame, fps, config: SPRING.heavy });
  const taglineProgress = spring({ frame, fps, delay: 12, config: SPRING.gentle });
  const ctaProgress = spring({ frame, fps, delay: 20, config: SPRING.pop });

  return (
    <AbsoluteFill style={{
      background: '#0f172a',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <div style={{ textAlign: 'center' }}>
        <h1 style={{
          fontSize: 72, fontWeight: 'bold', color: '#fff',
          opacity: headlineProgress,
          transform: `scale(${headlineProgress})`,
        }}>{headline}</h1>

        {tagline && (
          <p style={{
            fontSize: 28, color: 'rgba(255,255,255,0.6)', marginTop: 16,
            opacity: taglineProgress,
            transform: `translateY(${interpolate(taglineProgress, [0, 1], [15, 0])}px)`,
          }}>{tagline}</p>
        )}

        {ctaText && (
          <div style={{
            display: 'inline-block', marginTop: 32,
            background: accent, padding: '16px 40px', borderRadius: 8,
            fontSize: 24, fontWeight: 'bold', color: '#fff',
            transform: `scale(${ctaProgress})`, opacity: ctaProgress,
          }}>{ctaText}</div>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 9. Utility: useSpringTrail

Reusable hook for trail animations.

```tsx
import { spring, SpringConfig, useCurrentFrame, useVideoConfig } from 'remotion';

function useSpringTrail(
  count: number,
  config: Partial<SpringConfig>,
  staggerFrames = 4,
  baseDelay = 0,
) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return Array.from({ length: count }, (_, i) => {
    const delay = baseDelay + i * staggerFrames;
    return spring({ frame, fps, delay, config });
  });
}

// Usage:
const trail = useSpringTrail(5, SPRING.pop, 4);
// trail = [0.98, 0.85, 0.5, 0.1, 0] -- each item at different progress
```

## 10. Utility: useSpringEnterExit

Reusable hook for enter + exit pattern.

```tsx
function useSpringEnterExit(
  enterConfig: Partial<SpringConfig>,
  exitConfig: Partial<SpringConfig>,
  enterDelay = 0,
  exitBeforeEnd = 30,
) {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const enter = spring({ frame, fps, delay: enterDelay, config: enterConfig });
  const exit = spring({
    frame, fps,
    delay: durationInFrames - exitBeforeEnd,
    config: exitConfig,
  });

  return enter - exit;
}

// Usage:
const progress = useSpringEnterExit(SPRING.bouncy, SPRING.stiff, 0, 25);
```

---

## 11. Combining with Other Skills

```tsx
const CombinedScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgOpacity = spring({ frame, fps, config: SPRING.smooth });

  return (
    <AbsoluteFill>
      {/* react-animation: visual atmosphere */}
      <div style={{ opacity: bgOpacity }}>
        <Aurora colorStops={['#3A29FF', '#FF94B4']} />
      </div>

      {/* spring-animation: bouncy title entrance */}
      <SpringTitleCard title="Natural Motion" subtitle="Physics-driven beauty" />

      {/* gsap-animation: text splitting that spring can't do */}
      <GSAPTextReveal text="Advanced Typography" />
    </AbsoluteFill>
  );
};
```

| Skill | Best For |
|-------|----------|
| **spring-animation** | Bouncy entrances, elastic trails, organic physics, overshoot effects, spring counters |
| **gsap-animation** | Text splitting (SplitText), SVG drawing (DrawSVG), SVG morphing, complex timeline labels |
| **react-animation** | Visual backgrounds (Aurora, Silk, Particles), shader effects |

---

## 12. Composition Registration

```tsx
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="SpringTitleCard" component={SpringTitleCard}
      durationInFrames={90} fps={30} width={1920} height={1080}
      defaultProps={{ title: 'SPRING PHYSICS', subtitle: 'Natural motion for video' }} />
    <Composition id="SpringLowerThird" component={SpringLowerThird}
      durationInFrames={180} fps={30} width={1920} height={1080}
      defaultProps={{ name: 'Jane Smith', title: 'Creative Director' }} />
    <Composition id="SpringFeatureGrid" component={SpringFeatureGrid}
      durationInFrames={90} fps={30} width={1920} height={1080}
      defaultProps={{ features: [
        { icon: '🚀', label: 'Fast' },
        { icon: '🎯', label: 'Precise' },
        { icon: '✨', label: 'Beautiful' },
      ]}} />
    <Composition id="SpringOutro" component={SpringOutro}
      durationInFrames={120} fps={30} width={1920} height={1080}
      defaultProps={{ headline: 'GET STARTED', tagline: 'Try it free today', ctaText: 'Sign Up →' }} />
  </>
);
```

---

## 13. Rendering

```bash
# Default MP4
npx remotion render src/index.ts SpringTitleCard --output out/title.mp4

# High quality
npx remotion render src/index.ts SpringTitleCard --codec h264 --crf 15

# GIF
npx remotion render src/index.ts SpringTitleCard --codec gif --every-nth-frame 2

# ProRes for editing
npx remotion render src/index.ts SpringTitleCard --codec prores --prores-profile 4444
```
