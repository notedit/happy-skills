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
├── index.ts                # Entry point (registers GSAP plugins)
├── Root.tsx                # Composition registration
├── Composition.tsx         # Main video with TransitionSeries
├── gsap-setup.ts           # GSAP plugin registration (if using GSAP)
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
  fontFamily: 'Inter, system-ui, sans-serif',
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

```tsx
import { AbsoluteFill, Sequence } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { FluidBackground } from './components/FluidBackground';
import { SCENE_FRAMES, TRANSITION_FRAMES, COLORS } from './config';
// Import all scenes...

export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {/* Background persists across all scenes */}
      <FluidBackground />

      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.scene1}>
          <Scene1Hook />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        <TransitionSeries.Sequence durationInFrames={SCENE_FRAMES.scene2}>
          <Scene2Question />
        </TransitionSeries.Sequence>

        {/* ... remaining scenes with transitions */}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
```

---

## Scene Component Template

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { COLORS, TYPOGRAPHY } from '../config';

export const Scene1Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animation logic here
  const entrance = spring({ frame, fps, config: { damping: 12, stiffness: 120 } });

  return (
    <AbsoluteFill style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      {/* Scene content */}
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
