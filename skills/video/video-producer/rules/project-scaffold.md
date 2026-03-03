---
name: project-scaffold
description: Standard Remotion project structure and config templates for video production
metadata:
  tags: remotion, project, scaffold, config, structure
---

## Project Structure

```
src/
├── config.ts               # All video parameters (single source of truth)
├── spring-presets.ts        # Spring physics presets (ALWAYS included)
├── index.ts                # Entry point
├── Root.tsx                # Composition registration
├── Composition.tsx         # Main video with TransitionSeries
├── gsap-setup.ts           # GSAP plugin registration (only if using GSAP patterns)
├── components/
│   ├── FluidBackground.tsx # Persistent animated background
│   ├── BrowserMockup.tsx   # Browser window frame (if needed)
│   └── ...                 # Shared components
└── scenes/
    ├── Scene1Hook.tsx
    ├── Scene2Question.tsx
    ├── Scene3Reveal.tsx
    └── ...                 # One file per scene
```

**Note:** `spring-presets.ts` is always generated. `gsap-setup.ts` is only generated when GSAP patterns are used.

---

## config.ts Template

```tsx
export const VIDEO_CONFIG = {
  fps: 30,
  width: 1920,
  height: 1080,
};

export const SCENE_FRAMES = {
  scene1: 90,   // 3.0s - Hook
  scene2: 90,   // 3.0s - Question
  scene3: 75,   // 2.5s - Reveal
  scene4: 105,  // 3.5s - Benefit
  scene5: 90,   // 3.0s - Comparison
  scene6: 105,  // 3.5s - Demo
  scene7: 105,  // 3.5s - Showcase
  scene8: 90,   // 3.0s - CTA
};

export const TRANSITION_FRAMES = 15;

export const COLORS = {
  background: '#FFF5F0',
  textPrimary: '#1A1A1A',
  textSecondary: '#6B7280',
  accent: '#3B82F6',
  accentLight: 'rgba(59, 130, 246, 0.2)',
  surface: 'rgba(255, 255, 255, 0.65)',
  surfaceDark: '#1E1E2E',
};

export const TYPOGRAPHY = {
  fontFamily: '"Satoshi", "General Sans", sans-serif',  // See style-presets.md for per-preset fonts
  heroSize: 90,
  titleSize: 64,
  bodySize: 32,
  labelSize: 18,
  weight: { bold: 700, extraBold: 800, black: 900 },
};
```

Adjust `SCENE_FRAMES` values based on the narrative template's recommended durations. Multiply seconds by `VIDEO_CONFIG.fps`.

---

## Root.tsx Template

```tsx
import { Composition } from 'remotion';
import { MainVideo } from './Composition';
import { VIDEO_CONFIG, SCENE_FRAMES, TRANSITION_FRAMES } from './config';

const totalFrames = Object.values(SCENE_FRAMES).reduce((a, b) => a + b, 0)
  + (Object.keys(SCENE_FRAMES).length - 1) * TRANSITION_FRAMES;

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="MainVideo"
      component={MainVideo}
      durationInFrames={totalFrames}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
    />
    {/* Individual scene preview compositions */}
    <Composition
      id="Scene1-Preview"
      component={Scene1Hook}
      durationInFrames={SCENE_FRAMES.scene1}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
    />
    {/* ... repeat for each scene */}
  </>
);
```

Always register individual scene previews — this lets the user preview and iterate on each scene in the Remotion Studio without rendering the full video.

---

## Composition.tsx Template

**CRITICAL: Each scene inside `TransitionSeries` MUST have its own opaque background.** If you place `FluidBackground` outside `TransitionSeries` and scenes are transparent, `fade()` transitions will show BOTH scenes simultaneously — their content overlaps and creates a visual glitch. The fix is to wrap each scene with its own background layer.

```tsx
import { AbsoluteFill, Sequence } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { FluidBackground } from './components/FluidBackground';
import { SCENE_FRAMES, TRANSITION_FRAMES, COLORS } from './config';
// Import all scenes...

// Each scene gets its own opaque background to prevent transition overlap
const SceneWithBackground: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
    <FluidBackground />
    {children}
  </AbsoluteFill>
);

export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.scene1}>
          <SceneWithBackground>
            <Scene1Hook />
          </SceneWithBackground>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.scene2}>
          <SceneWithBackground>
            <Scene2Question />
          </SceneWithBackground>
        </TransitionSeries.Sequence>

        {/* ... remaining scenes with transitions */}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
```

**Why this works:** During a `fade()` transition, Remotion renders both the exiting and entering scenes simultaneously. The exiting scene fades out (opacity 1→0) while the entering scene fades in (opacity 0→1). If scenes lack their own opaque background, the content of both scenes bleeds through. By giving each scene its own `SceneWithBackground`, the entering scene's background properly covers the exiting scene during the crossfade.

---

## spring-presets.ts Template (ALWAYS generate)

```tsx
// src/spring-presets.ts
import { SpringConfig } from 'remotion';

export const SPRING = {
  smooth:   { damping: 200 } as Partial<SpringConfig>,
  snappy:   { damping: 20, stiffness: 200 } as Partial<SpringConfig>,
  bouncy:   { damping: 8 } as Partial<SpringConfig>,
  heavy:    { damping: 15, stiffness: 80, mass: 2 } as Partial<SpringConfig>,
  wobbly:   { damping: 4, stiffness: 80 } as Partial<SpringConfig>,
  stiff:    { damping: 15, stiffness: 300 } as Partial<SpringConfig>,
  gentle:   { damping: 20, stiffness: 40, mass: 1.5 } as Partial<SpringConfig>,
  molasses: { damping: 25, stiffness: 30, mass: 3 } as Partial<SpringConfig>,
  pop:      { damping: 6, stiffness: 150 } as Partial<SpringConfig>,
  rubber:   { damping: 3, stiffness: 100, mass: 0.5 } as Partial<SpringConfig>,
} as const;
```

Customize presets based on the video's emotional tone. See spring-animation skill `rules/spring-presets.md` for brand-specific and role-based config sets.

---

## Scene Component Template

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { COLORS, TYPOGRAPHY } from '../config';
import { SPRING } from '../spring-presets';

export const Scene1Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring-driven entrance (default for all scenes)
  const entrance = spring({ frame, fps, config: SPRING.bouncy });
  const titleY = interpolate(entrance, [0, 1], [50, 0]);

  return (
    <AbsoluteFill style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <h1 style={{
        opacity: entrance,
        transform: `translateY(${titleY}px)`,
      }}>
        {/* Scene content */}
      </h1>
    </AbsoluteFill>
  );
};
```

---

## FluidBackground Component

Standard animated gradient background. Use Remotion native `interpolate()` — no GSAP needed.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { COLORS } from '../config';

export const FluidBackground: React.FC<{ speed?: number }> = ({ speed = 1 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const blob1X = interpolate(frame * speed, [0, durationInFrames], [-200, 400]);
  const blob1Y = interpolate(frame * speed, [0, durationInFrames / 2, durationInFrames], [0, 150, 0]);
  const blob2X = interpolate(frame * speed, [0, durationInFrames], [800, 200]);
  const blob2Y = interpolate(frame * speed, [0, durationInFrames / 2, durationInFrames], [300, -100, 200]);

  return (
    <AbsoluteFill style={{ background: COLORS.background }}>
      <div style={{
        position: 'absolute', width: 900, height: 900,
        background: COLORS.accentLight, borderRadius: '50%',
        filter: 'blur(120px)', opacity: 0.7,
        transform: `translate(${blob1X}px, ${blob1Y}px)`,
      }} />
      <div style={{
        position: 'absolute', width: 800, height: 800,
        background: 'rgba(224, 195, 252, 0.5)', borderRadius: '50%',
        filter: 'blur(100px)', opacity: 0.6,
        transform: `translate(${blob2X}px, ${blob2Y}px)`,
      }} />
    </AbsoluteFill>
  );
};
```

Adjust blob colors to match the selected style preset.

---

## GSAP Setup (when using gsap-animation patterns)

```tsx
// src/gsap-setup.ts
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { CustomEase } from 'gsap/CustomEase';
// Import other plugins as needed

gsap.registerPlugin(SplitText, CustomEase);
export { gsap };
```

Only import plugins that are actually used in the video's scenes. See gsap-animation skill for the full plugin list.
