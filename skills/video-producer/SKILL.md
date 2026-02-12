---
name: video-producer
description: >
  End-to-end Remotion video production from natural language briefs.
  Orchestrates narrative structure, scene animation, visual style, and rendering
  to produce complete promotional videos. Use when a user wants to create a
  complete video (product promo, typographic piece, social media animation) —
  not just individual animation effects. Coordinates gsap-animation and
  react-animation skills as building blocks.
---

## When to use

Use this skill when the user provides a **video brief** — a description of a complete video with multiple scenes or a narrative arc.

**Triggers:** "create a promo video", "make a product demo", "I need a 30-second ad", "build a social media animation", or any prompt describing a multi-scene video.

**Do NOT use for:**
- Single animation effects → use `gsap-animation`
- Visual background components → use `react-animation`
- Non-video tasks

## Skill Relationships

```
video-producer (this skill)       ← orchestration: what story, which scenes
├── gsap-animation                ← animation: text splits, 3D transforms, timelines
├── react-animation               ← visuals: Aurora, Silk, particles, grain
└── Remotion                      ← engine: rendering, composition, sequences
```

## Workflow

Initial request: $ARGUMENTS

### Phase 1: Brief Intake

Extract from the user's request. Use AskUserQuestion for any missing **required** fields.

| Field | Required | Default | Example |
|-------|:--------:|---------|---------|
| Product / brand name | Yes | — | "Topview" |
| Video type | Yes | SaaS Promo | SaaS Promo / Typographic / Social Overlay |
| Core messages (2-4) | Yes | — | "AI-powered editing", "No coding required" |
| Target audience | No | General | "Developers", "Marketers" |
| Duration | No | Template default | "25 seconds" |
| Resolution | No | 1920x1080 | 1080x1080 for square |
| FPS | No | 30 | 60 for social media |
| Visual style | No | Apple Minimal | Apple Minimal / Bold Typography / Dark Tech |
| CTA text | No | None | "Start Creating →" |
| Color accent | No | From style preset | "#FF7D00" |

### Phase 2: Planning

1. **Select narrative template** based on video type → see `rules/narrative-templates.md`
2. **Select visual style** → see `rules/style-presets.md`
3. **Map user's messages to scene slots** in the selected template
4. **Select animation pattern** for each scene → see `rules/scene-patterns.md`
5. Present the plan as a table to the user:

```
Scene | Duration | Pattern        | Content
1     | 3s       | TitleCard      | "Topview is powerful"
2     | 3s       | CardFlip3D     | CLI pain → AI solution
...
```

Wait for user confirmation before proceeding.

### Phase 3: Project Scaffold

Generate the standard Remotion project structure → see `rules/project-scaffold.md`:

1. `src/config.ts` — all parameters (colors, typography, scene frames)
2. `src/Root.tsx` — composition registration
3. `src/Composition.tsx` — TransitionSeries with all scenes
4. `src/components/` — shared components (background, etc.)
5. `src/scenes/` — one file per scene

**Frame calculation:** `sceneFrames = Math.ceil(sceneDurationSeconds * fps)`

### Phase 4: Scene Implementation

Implement scenes in order. For each scene:

1. Create `src/scenes/SceneN_Name.tsx`
2. Select the right hook:
   - Complex timeline / text splitting / 3D transforms → `useGSAPTimeline` or `useGSAPWithFonts` (from gsap-animation skill)
   - Simple fades / slides / counters → Remotion native `interpolate()` + `spring()`
   - Visual backgrounds → react-animation components
3. Apply the selected animation pattern from the plan
4. Wire into `Composition.tsx`

**Pattern selection principle:** Use Remotion native for anything `interpolate()` handles cleanly. Use GSAP only for SplitText, DrawSVG, MorphSVG, complex timeline orchestration, 3D transforms, and registered effects.

### Phase 5: Rendering

```bash
# Standard MP4
npx remotion render src/index.ts MainVideo --output out/video.mp4

# High quality
npx remotion render src/index.ts MainVideo --codec h264 --crf 15

# Transparent background (social overlays)
npx remotion render src/index.ts MainVideo --codec prores --prores-profile 4444
npx remotion render src/index.ts MainVideo --codec vp9 --output out/overlay.webm
```

| Format | Alpha | Use Case |
|--------|:-----:|----------|
| MP4 H.264 | No | Universal playback |
| ProRes 4444 | Yes | Professional compositing |
| WebM VP9 | Yes | Web overlays |

## Quick Decision Reference

| "I need..." | Use |
|-------------|-----|
| Bold text entrance | gsap: charCascade / textReveal effect |
| Side-by-side comparison | gsap: SplitScreenComparison template |
| Card flip reveal | gsap: CardFlip3D template |
| Elements from both sides | gsap: PerspectiveEntrance template |
| Word highlighting | gsap: TextHighlightBox pattern |
| UI click simulation | gsap: CursorClick pattern |
| Text swap animation | gsap: RotateXTextSwap pattern |
| Flowing background | react-animation: Aurora / Silk |
| Film grain overlay | react-animation: NoiseOverlay |
| Simple fade / slide | Remotion: interpolate() |
| Number counter | Remotion: interpolate() |
| Typing effect | Remotion: .slice() + interpolate() |
| Scene transition | gsap: circleReveal / wipeIn effect |
| Logo stroke draw | gsap: DrawSVG + drawIn effect |
