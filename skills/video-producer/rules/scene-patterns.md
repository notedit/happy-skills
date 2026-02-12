---
name: scene-patterns
description: Mapping from scene purposes to specific animation implementations
metadata:
  tags: video, scenes, patterns, gsap, remotion, animation
---

## Pattern Selection Principle

```
Can interpolate() do it cleanly?
├── Yes → Use Remotion native (simpler, deterministic)
└── No → Does it need text splitting, SVG, or complex timeline?
    ├── Text splitting → gsap-animation: useGSAPWithFonts
    ├── SVG morph/draw → gsap-animation: useGSAPTimeline
    ├── 3D transforms → gsap-animation: useGSAPTimeline
    ├── Multi-step timeline → gsap-animation: useGSAPTimeline
    └── Visual atmosphere → react-animation component
```

---

## Scene Purpose → Pattern Mapping

### Text Scenes

| Purpose | Pattern | Source | Hook | Key Props |
|---------|---------|--------|------|-----------|
| Bold title entrance | TitleCard | gsap-animation template | useGSAPWithFonts | mainTitle, subtitle |
| Character-by-character | charCascade | gsap-animation effect | useGSAPWithFonts | — |
| Line-by-line reveal | textReveal | gsap-animation effect | useGSAPWithFonts | — |
| Decode / scramble | ScrambleText | gsap-animation pattern | useGSAPTimeline | text, chars |
| Highlight keywords | TextHighlightBox | gsap-animation pattern | useGSAPWithFonts | text, highlights[] |
| Swap two messages | RotateXTextSwap | gsap-animation template | useGSAPWithFonts | textOut, textIn |
| Typing effect | .slice() | Remotion native | — | text, speed |
| Number counter | AnimatedCounter | Remotion native | — | endValue, prefix, suffix |
| Closing / CTA | Outro | gsap-animation template | useGSAPWithFonts | headline, tagline |

### Reveal & Transform Scenes

| Purpose | Pattern | Source | Hook | Key Props |
|---------|---------|--------|------|-----------|
| Card flip reveal | CardFlip3D | gsap-animation template | useGSAPTimeline | frontContent, backContent |
| Two-sided convergence | PerspectiveEntrance | gsap-animation template | useGSAPTimeline | leftContent, rightContent |
| Before/after comparison | SplitScreenComparison | gsap-animation template | useGSAPTimeline | leftPanel, rightPanel, dimLeft |
| Logo stroke draw | LogoReveal + drawIn | gsap-animation template | useGSAPTimeline | svgContent, text |
| Shape morphing | MorphSVG | gsap-animation pattern | useGSAPTimeline | source path, target path |

### Interaction Scenes

| Purpose | Pattern | Source | Hook | Key Props |
|---------|---------|--------|------|-----------|
| Simulated click | CursorClick | gsap-animation template | useGSAPTimeline | targetSelector |
| UI mockup | Custom (browser window) | Manual implementation | Remotion native | — |
| Chat interface | Custom (chat bubbles) | Manual implementation | Remotion native | — |

### Transition & Visual Scenes

| Purpose | Pattern | Source | Hook |
|---------|---------|--------|------|
| Circle reveal | circleReveal | gsap-animation effect | useGSAPTimeline |
| Wipe | wipeIn | gsap-animation effect | useGSAPTimeline |
| Crossfade | TransitionSeries + fade() | Remotion native | — |
| Slide transition | TransitionSeries + slide() | Remotion native | — |
| Fluid gradient bg | FluidBackground | Manual (interpolate) | Remotion native |
| Aurora / silk bg | Aurora / Silk | react-animation | — |
| Film grain overlay | NoiseOverlay | react-animation | — |

---

## Common Scene Recipes

### Recipe: Hook Scene (SaaS Promo Scene 1)

Two-phase: perspective entrance → rotateX text swap.

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

### Recipe: Showcase Grid (SaaS Promo Scene 7)

Remotion native — no GSAP needed.

```tsx
const ShowcaseGrid: React.FC<{ items: GridItem[] }> = ({ items }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Grid with staggered entrance
  return (
    <AbsoluteFill style={{
      perspective: 1200,
      transform: `rotateX(35deg) rotateZ(-8deg) scale(1.8)`,
    }}>
      {items.map((item, i) => {
        const delay = i * 4;
        const entrance = spring({ frame: frame - delay, fps, config: { damping: 12 } });
        const scale = interpolate(entrance, [0, 1], [0.6, 1]);
        // Diagonal scroll
        const scrollX = frame * 1.2;
        const scrollY = frame * 0.7;
        return (
          <div key={i} style={{
            transform: `translate(${scrollX}px, ${scrollY}px) scale(${scale})`,
            opacity: entrance,
          }}>
            <GridCard {...item} />
          </div>
        );
      })}
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
