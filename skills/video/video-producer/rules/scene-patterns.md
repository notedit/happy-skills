---
name: scene-patterns
description: Mapping from scene purposes to specific animation implementations
metadata:
  tags: video, scenes, patterns, gsap, remotion, animation
---

## Pattern Selection Principle

```
What kind of motion do I need?
├── Bouncy / elastic / organic feel?
│   └── spring-animation: spring() + SPRING presets
│       ├── Entrances → ScalePop, SpringEntrance, CharacterTrail, WordTrail
│       ├── Staggered reveals → SpringTrail, GridStagger
│       ├── Sequential → useSpringChain
│       ├── Enter + exit → useSpringEnterExit
│       ├── Counters with overshoot → SpringCounter
│       └── Scene transitions → SpringSlide, SpringCrossfade
├── Text splitting / SVG / complex timeline?
│   └── gsap-animation: useGSAPTimeline / useGSAPWithFonts
│       ├── Char/word/line splitting → SplitText
│       ├── SVG stroke drawing → DrawSVG
│       ├── SVG morphing → MorphSVG
│       ├── Decode effects → ScrambleText
│       └── Timeline with labels → gsap.timeline()
├── Simple linear / eased motion?
│   └── Remotion: interpolate()
│       ├── Linear fade/slide
│       ├── Typing effect (.slice())
│       └── Progress bars
└── Visual atmosphere?
    └── react-animation: Aurora, Silk, Particles, NoiseOverlay
```

**Default rule:** Start with `spring()`. Only escalate to GSAP when you need SplitText, DrawSVG, MorphSVG, or ScrambleText. Only use raw `interpolate()` for strictly linear motion.

---

## Scene Purpose → Pattern Mapping

### Text Scenes

| Purpose | Pattern | Source | When to Choose |
|---------|---------|--------|---------------|
| Bold title (bouncy words) | SpringTitleCard / WordTrail | spring-animation | **Default.** Bouncy, organic feel |
| Bold title (split chars with mask) | TitleCard / charCascade | gsap-animation | Need char-level mask reveal or SplitText features |
| Character trail (simple) | CharacterTrail | spring-animation | Per-char spring stagger, no mask needed |
| Character reveal (mask) | charCascade | gsap-animation | Need overflow:hidden mask per char/line |
| Line-by-line reveal (mask) | textReveal | gsap-animation | Need line-level mask reveal |
| Decode / scramble | ScrambleText | gsap-animation | Unique effect, GSAP-only |
| Highlight keywords | TextHighlightBox | gsap-animation | Need word-level positioning via SplitText |
| Swap two messages | RotateXTextSwap | gsap-animation | 3D rotateX text swap |
| Typing effect | .slice() | Remotion native | Linear typewriter |
| Number counter (linear) | AnimatedCounter | Remotion native | Smooth, no overshoot |
| Number counter (bouncy) | SpringCounter | spring-animation | **Preferred.** Overshoots then settles |
| Closing / CTA (bouncy) | SpringOutro | spring-animation | **Default.** Pop-in CTA |
| Closing / CTA (SVG logo) | Outro | gsap-animation | Need DrawSVG logo reveal |

### Reveal & Transform Scenes

| Purpose | Pattern | Source | When to Choose |
|---------|---------|--------|---------------|
| Card flip (spring physics) | SpringCardFlip | spring-animation | **Default.** Weighty, natural flip feel |
| Card flip (smooth timeline) | CardFlip3D | gsap-animation | Need precise timeline control with labels |
| Perspective tilt entrance | PerspectiveTilt | spring-animation | Single element tilts in with weight |
| Two-sided convergence | PerspectiveEntrance | gsap-animation | Two elements enter from opposite sides |
| Before/after comparison | SplitScreenComparison | gsap-animation | Side-by-side with dim effect |
| Logo stroke draw | LogoReveal + drawIn | gsap-animation | GSAP-only (DrawSVG) |
| Shape morphing | MorphSVG | gsap-animation | GSAP-only (MorphSVG) |
| Staggered grid reveal | GridStagger | spring-animation | **Default for grids.** Center-out pop |
| Staggered list reveal | SpringTrail | spring-animation | **Default for lists.** Sequential pop |
| Feature showcase | SpringFeatureGrid | spring-animation | Icon + label grid with pop stagger |

### Interaction Scenes

| Purpose | Pattern | Source | When to Choose |
|---------|---------|--------|---------------|
| Simulated click | CursorClick | gsap-animation | GSAP-only (cursor path + ripple) |
| UI mockup elements | ScalePop / SpringEntrance | spring-animation | Bouncy element entrances in mockup |
| Chat bubbles | SpringTrail | spring-animation | Staggered bubble pop-in |

### Transition & Visual Scenes

| Purpose | Pattern | Source | When to Choose |
|---------|---------|--------|---------------|
| Circle reveal / iris | circleReveal | gsap-animation | Clip-path animation (GSAP-only) |
| Wipe | wipeIn | gsap-animation | Clip-path animation (GSAP-only) |
| Spring slide transition | SpringSlide | spring-animation | **Default.** Bouncy slide between scenes |
| Spring crossfade | SpringCrossfade | spring-animation | Smooth crossfade with spring scale |
| Crossfade (linear) | TransitionSeries + fade() | Remotion native | Simple, no bounce |
| Slide (linear) | TransitionSeries + slide() | Remotion native | Simple, no bounce |
| Fluid gradient bg | FluidBackground | Manual (interpolate) | Slow blob drift |
| Aurora / silk bg | Aurora / Silk | react-animation | Rich visual atmosphere |
| Film grain overlay | NoiseOverlay | react-animation | Organic texture |

---

## Common Scene Recipes

### Recipe: Hook Scene (SaaS Promo Scene 1) — Spring Version

Spring-driven two-phase entrance. Bouncy, organic feel.

```tsx
import { spring, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { SPRING } from '../spring-presets';

// Phase 1: Two elements enter from sides with spring physics
const leftEntrance = spring({ frame, fps, config: SPRING.bouncy });
const rightEntrance = spring({ frame, fps, delay: 4, config: SPRING.bouncy });
const leftX = interpolate(leftEntrance, [0, 1], [-600, 0]);
const rightX = interpolate(rightEntrance, [0, 1], [600, 0]);

// Phase 2: First text exits, second springs in
const exitProgress = spring({ frame, fps, delay: 50, config: SPRING.stiff });
const newEntrance = spring({ frame, fps, delay: 55, config: SPRING.pop });
const exitOpacity = 1 - exitProgress;
const exitY = interpolate(exitProgress, [0, 1], [0, -40]);
const newY = interpolate(newEntrance, [0, 1], [40, 0]);
```

### Recipe: Hook Scene — GSAP Version (when SplitText needed)

Use GSAP when you need char-level mask reveals that spring can't do.

```tsx
// Phase 1: Two elements enter from sides (frames 0-50)
const entrance = spring({ frame, fps, config: { damping: 14, stiffness: 120 } });
const leftX = interpolate(entrance, [0, 1], [-600, 0]);
const leftRotateY = interpolate(entrance, [0, 1], [60, 0]);
const rightX = interpolate(entrance, [0, 1], [600, 0]);
const rightRotateY = interpolate(entrance, [0, 1], [-60, 0]);

// Phase 2: First text exits backward, second falls in (frames 50-90)
const exitProgress = frame >= 50 ? interpolate(frame, [50, 65], [0, 1], { extrapolateRight: 'clamp' }) : 0;
const exitRotateX = interpolate(exitProgress, [0, 1], [0, 90]);
const newEntrance = frame >= 55 ? spring({ frame: frame - 55, fps }) : 0;
const newRotateX = interpolate(newEntrance, [0, 1], [-90, 0]);
```

### Recipe: Card Flip Scene (SaaS Promo Scene 2)

```tsx
// Use gsap-animation CardFlip3D template
<CardFlip3D
  frontContent={<TerminalMockup lines={painPointLines} />}
  backContent={<UIPreview screenshot={productUI} />}
  flipDelay={1.5}
  flipDuration={1.2}
/>
```

### Recipe: Comparison Scene (SaaS Promo Scene 4-5)

```tsx
// Scene 4: Equal comparison
<SplitScreenComparison
  leftPanel={<OldWayContent />}
  rightPanel={<NewWayContent />}
  leftLabel="Before"
  rightLabel="After"
  centerElement="VS"
/>

// Scene 5: Winner highlight
<SplitScreenComparison
  leftPanel={<OldWayContent />}
  rightPanel={<NewWayContent />}
  dimLeft={true}
  hold={1.5}
/>
```

### Recipe: Showcase Grid (SaaS Promo Scene 7) — Spring Version

Spring-animation GridStagger for feature showcase. Center-out pop-in.

```tsx
import { SPRING } from '../spring-presets';

const ShowcaseGrid: React.FC<{ items: GridItem[] }> = ({ items }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const columns = 3;
  const centerCol = (columns - 1) / 2;
  const rows = Math.ceil(items.length / columns);
  const centerRow = (rows - 1) / 2;

  return (
    <AbsoluteFill style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <div style={{ display: 'grid', gridTemplateColumns: `repeat(${columns}, 240px)`, gap: 24 }}>
        {items.map((item, i) => {
          const col = i % columns;
          const row = Math.floor(i / columns);
          const dist = Math.sqrt((col - centerCol) ** 2 + (row - centerRow) ** 2);
          const delay = Math.round(dist * 5);
          const scale = spring({ frame, fps, delay, config: SPRING.pop });
          const opacity = spring({ frame, fps, delay, config: SPRING.smooth });

          return (
            <div key={i} style={{
              transform: `scale(${scale})`,
              opacity,
              background: 'rgba(255,255,255,0.06)',
              borderRadius: 16, padding: 24, textAlign: 'center',
            }}>
              <GridCard {...item} />
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

### Recipe: CTA with Click (SaaS Promo Scene 8)

```tsx
// Combine Outro template with CursorClick
<AbsoluteFill>
  <Outro headline={brandName} tagline={slogan} />
  <Sequence from={Math.round(fps * 2)}>
    <CursorClick targetSelector=".cta-button" cursorDelay={0.3} clickDelay={0.8}>
      <CTAButton text="Start Creating →" />
    </CursorClick>
  </Sequence>
</AbsoluteFill>
```

---

## UI Mockup Components

Commonly needed but not in animation skills — implement manually:

**Browser Window:** Dark frame with 3 dots (red/yellow/green), 36px toolbar, 24px border-radius, deep shadow. Content area renders children.

**Terminal:** Dark background (#1a1a2e), monospace font, green command text (#4ade80), gray comment text (#6b7280). Lines appear with staggered opacity.

**Chat Interface:** Left sidebar (gray), right content area. Chat bubbles with spring entrance. Typing indicator with 3 pulsing dots.

**Mobile Frame:** Rounded rectangle with notch, status bar. Content area renders children at mobile aspect ratio.
