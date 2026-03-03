---
name: video-producer
description: >
  End-to-end Remotion video production from natural language briefs.
  Orchestrates narrative structure, scene animation, visual style, and rendering
  to produce complete promotional videos. Use when a user wants to create a
  complete video (product promo, typographic piece, social media animation) —
  not just individual animation effects. Coordinates gsap-animation,
  spring-animation, and react-animation skills as building blocks.
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
├── gsap-animation                ← animation: text splits, SVG drawing, timeline orchestration
├── spring-animation              ← physics: bouncy entrances, elastic trails, organic motion
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
| Emotional tone | Yes | — | Urgent / Reassuring / Exciting / Professional / Rebellious / Warm / Playful |
| Memory anchor | Yes | — | "The single image viewers will remember 30s later" |
| Target audience | No | General | "Developers", "Marketers" |
| Duration | No | Template default | "25 seconds" |
| Resolution | No | 1920x1080 | 1080x1080 for square |
| FPS | No | 30 | 60 for social media |
| Visual style | No | Apple Minimal | Apple Minimal / Bold Typography / Dark Tech / Warm Organic / Retro Pop / Editorial Mono |
| CTA text | No | None | "Start Creating →" |
| Color accent | No | From style preset | "#FF7D00" |

**Emotional tone** drives animation technique selection, spring config, and pacing:
- **Urgent** → `SPRING.stiff` + GSAP hard cuts, fast stagger (2-3 frames), `power3.out` for GSAP scenes
- **Reassuring** → `SPRING.smooth` / `SPRING.gentle`, high damping, slow reveals, warm palette
- **Exciting** → `SPRING.bouncy` / `SPRING.pop`, low damping, saturated colors, SpringTrail pop-ins
- **Professional** → `SPRING.snappy` / `SPRING.smooth`, measured timing, clean motion, generous holds
- **Rebellious** → `SPRING.stiff` + `SPRING.rubber` mix, GSAP glitch effects, irregular stagger
- **Warm** → `SPRING.gentle` / `SPRING.molasses`, warm gradients, rounded shapes, slow stagger (6-8 frames)
- **Playful** → `SPRING.wobbly` / `SPRING.rubber`, extreme overshoot, GridStagger center-out, bright accents

**Memory anchor** — the ONE visual moment viewers will screenshot or recall. Every production decision should reinforce this anchor. Ask: "If someone describes this video to a friend, what image do they describe?"

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

### Phase 4: Scene Implementation + Evaluation

Implement scenes in order. Each scene goes through a **build → verify → fix** loop before moving to the next. → see `rules/scene-evaluator.md` for the full scoring rubric and auto-fix rules.

For each scene:

**Step 4a: Implement scene**

1. Create `src/scenes/SceneN_Name.tsx`
2. Select the right technique:
   - Text splitting / SVG drawing / complex timelines → `useGSAPTimeline` or `useGSAPWithFonts` (from gsap-animation skill)
   - Bouncy/elastic entrances / spring trails / overshoot effects → `spring()` + presets (from spring-animation skill)
   - Simple fades / slides / linear counters → Remotion native `interpolate()`
   - Visual backgrounds → react-animation components
3. Apply the selected animation pattern from the plan
4. Wire into `Composition.tsx` and register preview in `Root.tsx`

**Step 4b: Render stills**

Capture two key frames for visual inspection:

```bash
# Entry frame — catches early layout, initial positions
npx remotion still src/index.ts SceneN-Preview /tmp/sceneN_entry.png --frame={floor(SCENE_FRAMES.sceneN * 0.15)}

# Peak frame — hero moment, all entrances settled
npx remotion still src/index.ts SceneN-Preview /tmp/sceneN_peak.png --frame={floor(SCENE_FRAMES.sceneN * 0.60)}
```

**Step 4c: Evaluate**

Read the scene code + `config.ts` + rendered screenshots. Score across 7 weighted dimensions (anti-pattern compliance, typography, color & contrast, motion design, composition, narrative coherence, technical correctness).

- **Score >= 7.0** and no instant-fails → **PASS**, proceed to next scene
- **Score < 7.0** or instant-fail triggered → proceed to Step 4d

**Step 4d: Auto-fix** (max 2 iterations)

Apply targeted fixes from the deduction → fix mapping table in `rules/scene-evaluator.md`. Each deduction maps to a concrete code change — not a vague suggestion. After fixing:

- Return to **Step 4b** (re-render stills, re-score)
- After **iteration 2**, if still below threshold: emit **WARNING** and proceed to next scene

**Cross-scene tracking:** Maintain a running context of accent colors, spring presets, entrance directions, and techniques used per scene. At scene 3+, check for variety issues (same preset 3x in a row, same entrance direction, etc.).

**After all scenes complete:** Output a full **Evaluation Summary Table** showing per-scene scores, iteration counts, and cross-scene notes before proceeding to Phase 5.

**Pattern selection principle:** Use `spring()` for physics-driven motion with bounce/overshoot. Use GSAP for SplitText, DrawSVG, MorphSVG, and complex timeline orchestration. Use `interpolate()` for simple linear/eased motion.

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

## Complexity Calibration

Match implementation complexity to the emotional tone and visual style. The effort invested in animation must serve the creative vision — not exceed or undercut it.

| Tone × Style | Pacing | Spring Preset | GSAP Usage | Hold Duration |
|---|---|---|---|---|
| Urgent + Bold Typography | Fast (1.5-2.5s scenes) | `stiff` (stagger: 2f) | charCascade, hard cut transitions | Short (0.5s) |
| Exciting + Dark Tech | Medium-fast (2-3s) | `bouncy` / `pop` (stagger: 3f) | circleReveal transitions, DrawSVG | Medium (0.8s) |
| Professional + Apple Minimal | Measured (3-4s) | `smooth` / `snappy` (stagger: 5f) | textReveal, SplitScreenComparison | Long (1.2s) |
| Warm + Warm Organic | Slow (3-5s) | `gentle` / `molasses` (stagger: 8f) | Minimal GSAP, prefer spring-only | Long (1.5s) |
| Rebellious + Retro Pop | Irregular | `stiff` + `rubber` alternating | ScrambleText, glitch effects | Variable |
| Playful + any | Bouncy (2-3s) | `wobbly` / `pop` (stagger: 3f) | Minimal GSAP, SpringTrail + GridStagger | Medium (0.8s) |

**Principle:** One signature transition executed perfectly creates more impact than six mediocre effects. Invest animation budget in the memory anchor moment.

**Anti-bloat rule:** Each scene should use ONE dominant animation technique:
- Spring-dominant: `spring()` + `interpolate()` for all motion (bouncy entrances, trails, counters)
- GSAP-dominant: `useGSAPTimeline` for text splits, SVG operations, complex orchestration
- Mixed: Spring for element entrances, GSAP for text splitting within that element (acceptable)
- NEVER: GSAP timeline + spring physics + react-animation background + complex interpolations in one scene

**Spring-first principle:** Default to `spring()` for all entrances, exits, and stagger animations. Only add GSAP when you specifically need SplitText, DrawSVG, MorphSVG, ScrambleText, or complex timeline labels. Spring is lighter, requires no additional dependency, and produces naturally organic motion.

## Creative Direction Principles

**Every video must have a point of view.** A "clean, professional" video without a strong aesthetic commitment is just a generic video. Commit to specific, bold choices:

- A **color** that dominates (not 5 equally-weighted pastels)
- A **font** that has character (not the first Google Font result)
- A **motion signature** that repeats across scenes (the same easing curve, the same entrance direction, the same hold rhythm)
- A **spatial rule** that breaks expectations (all text left-aligned at 20%, asymmetric panels, diagonal grid)

**The Memorability Test:** Before finalizing the plan, ask: "If I showed this next to 10 other AI-generated promo videos, would mine look distinctly different?" If no, push the aesthetic further.

## Quick Decision Reference

| "I need..." | Use |
|-------------|-----|
| Bold text entrance (split chars) | gsap: charCascade / textReveal effect |
| Bold text entrance (bouncy words) | spring: WordTrail / CharacterTrail |
| Side-by-side comparison | gsap: SplitScreenComparison template |
| Card flip reveal (smooth) | gsap: CardFlip3D template |
| Card flip reveal (spring physics) | spring: SpringCardFlip |
| Elements from both sides | gsap: PerspectiveEntrance template |
| Word highlighting | gsap: TextHighlightBox pattern |
| UI click simulation | gsap: CursorClick pattern |
| Text swap animation | gsap: RotateXTextSwap pattern |
| Flowing background | react-animation: Aurora / Silk |
| Film grain overlay | react-animation: NoiseOverlay |
| Simple fade / slide | Remotion: interpolate() |
| Number counter (linear) | Remotion: interpolate() |
| Number counter (overshoot) | spring: SpringCounter |
| Bouncy scale entrance | spring: ScalePop |
| Staggered list/grid reveal | spring: SpringTrail / GridStagger |
| Enter + exit animation | spring: useSpringEnterExit |
| Sequential orchestration | spring: useSpringChain |
| Typing effect | Remotion: .slice() + interpolate() |
| Scene transition (wipe/iris) | gsap: circleReveal / wipeIn effect |
| Scene transition (spring slide) | spring: SpringSlide / SpringCrossfade |
| Logo stroke draw | gsap: DrawSVG + drawIn effect |
| Feature grid pop-in | spring: SpringFeatureGrid |

---

## Variability Enforcement

NEVER produce the same aesthetic twice across different videos. Each production must feel like a unique creative work, not a template fill-in.

- **Rotate fonts:** Never use the same display font in consecutive videos. If you used Space Grotesk last time, pick Clash Display or Cabinet Grotesk this time.
- **Rotate color temperature:** Alternate between warm (orange/coral/gold) and cool (blue/violet/emerald) dominant palettes.
- **Rotate spatial composition:** If the last video was center-aligned symmetrical, make this one left-anchored asymmetrical.
- **Rotate motion signatures:** Vary between spring-heavy, linear-mechanical, and organic-fluid animation philosophies.
- **Rotate background treatments:** Cycle through solid, gradient blob, aurora, grain texture, geometric pattern.

**The Divergence Rule:** Before starting Phase 3, mentally compare the planned aesthetic to a "default AI video" — white background, centered Inter text, fade-in transitions, blue accent. If your plan shares more than ONE of these traits, push further from the default.

---

## Creative Ambition

Every video should make viewers want to screenshot a frame and share it. This is motion graphics as a craft — not template assembly.

Push beyond "functional" toward "remarkable." Use unexpected font pairings. Try color combinations that feel risky. Let one scene break the grid. Give the memory anchor moment 2x the animation investment of other scenes.

The gap between a forgettable promo and a memorable one is not technical complexity — it's creative courage. Make bold choices and execute them with precision.
