---
name: scene-evaluator
description: Post-implementation quality gate that scores scenes against a rubric and auto-fixes issues
metadata:
  tags: video, quality, evaluation, scoring, auto-fix
---

## Overview

After each scene is implemented in Phase 4, run a self-evaluation loop:

```
Implement → Render Stills → Score → Pass or Fix → Next Scene
```

Maximum **2 fix iterations** per scene. If still below threshold after iteration 2, emit a WARNING and proceed.

---

## Key Frame Selection

Render two Remotion stills per scene for visual inspection:

| Frame | Formula | Purpose |
|-------|---------|---------|
| Entry frame | `floor(SCENE_FRAMES.sceneN * 0.15)` | Catches early layout, initial positions, background rendering |
| Peak frame | `floor(SCENE_FRAMES.sceneN * 0.60)` | Hero moment — all entrances settled, highlights active, peak composition |

**Remotion still command:**

```bash
npx remotion still src/index.ts SceneN-Preview /tmp/sceneN_entry.png --frame={entryFrame}
npx remotion still src/index.ts SceneN-Preview /tmp/sceneN_peak.png --frame={peakFrame}
```

Requires that `Root.tsx` registers individual scene preview compositions (e.g., `Scene1-Preview`, `Scene2-Preview`). See `rules/project-scaffold.md` Root.tsx template.

---

## Scoring Rubric

### 7 Dimensions (weighted score, 0-10 each)

| # | Dimension | Weight | Input Source |
|---|-----------|--------|-------------|
| 1 | Anti-Pattern Compliance | 20% | Code review (fonts, colors, composition) |
| 2 | Typography Quality | 15% | Code (sizes, weights, ratios, font choices) |
| 3 | Color & Contrast | 15% | Screenshot + code |
| 4 | Motion Design | 15% | Code (spring configs, stagger, variety) |
| 5 | Composition & Layout | 15% | Screenshot (balance, overflow, hierarchy) |
| 6 | Narrative Coherence | 10% | Code vs Phase 2 plan |
| 7 | Technical Correctness | 10% | Remotion still render success + code |

**Weighted score formula:**

```
total = (D1 * 0.20) + (D2 * 0.15) + (D3 * 0.15) + (D4 * 0.15) + (D5 * 0.15) + (D6 * 0.10) + (D7 * 0.10)
```

### Thresholds

| Weighted Score | Instant-Fail? | Verdict |
|---------------|:-------------:|---------|
| >= 7.0 | No | **PASS** — proceed to next scene |
| >= 7.0 | Yes | **AUTO-FIX** — fix instant-fail items only |
| < 7.0 | Either | **AUTO-FIX** — fix top deductions (max 2 iterations) |

---

## Instant-Fail Rules

These force a fix iteration regardless of the overall score:

| Rule | Detection | Fix |
|------|-----------|-----|
| Blacklisted display font (Inter, Roboto, Arial, Helvetica, Montserrat, Poppins, Nunito, system-ui) | Grep `fontFamily` in scene code | Replace with style preset's recommended font from Creative Typography Guide |
| Remotion still render fails | Still command exits non-zero | Fix the compilation/runtime error in scene code |
| Primary text unreadable against background | Screenshot: hero text < 3:1 contrast ratio estimate | Adjust text color or add text shadow / background overlay |

---

## Dimension 1: Anti-Pattern Compliance (Weight: 20%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| Blacklisted font as display font | -10 (instant-fail) | Grep `fontFamily` for Inter/Roboto/Arial/Helvetica/Montserrat/Poppins/Nunito/system-ui |
| Purple-to-blue gradient on white background | -4 | Code: gradient colors in blue-purple range + white/light background |
| Every element fades in with same timing | -3 | Code: all elements use identical `delay` or no stagger |
| Pure white (#FFFFFF) or pure black (#000000) background with no texture | -2 | Code: background color is exact #FFF/#000 with no FluidBackground/Aurora/NoiseOverlay |
| Same entrance animation on all text blocks | -2 | Code: hero text and body text use identical spring config + direction |
| Everything center-aligned symmetrically | -2 | Code: all elements use `textAlign: 'center'` + `justifyContent: 'center'` without variation |

## Dimension 2: Typography Quality (Weight: 15%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| Display/body size ratio below 2x | -3 | Code: `heroSize / bodySize < 2.0` |
| No weight contrast (display and body same weight) | -3 | Code: display and body use same font-weight value |
| Line height too loose for display text (> 1.2 for bold typography) | -2 | Code: display text `lineHeight > 1.2` when using Bold Typography preset |
| Missing font-weight specification (relying on defaults) | -2 | Code: no explicit `fontWeight` on text elements |
| Body text too large (> 36px at 1920w) | -1 | Code: body font-size exceeds 36px |
| Label/caption text same size as body | -1 | Code: label and body sizes are identical |

## Dimension 3: Color & Contrast (Weight: 15%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| Primary text unreadable against background | -10 (instant-fail) | Screenshot: text blends into background |
| No dominant accent — all colors equally weighted | -3 | Code: 3+ accent colors used without one clearly dominant |
| Accent color is safe blue (#3B82F6, #6366F1) as only color | -2 | Code: accent matches common safe blues |
| Text on image/gradient without shadow or overlay | -2 | Code + screenshot: text placed over varying background without readability aid |
| Insufficient contrast between secondary text and background | -2 | Screenshot: secondary text barely visible |
| Accent used on > 50% of elements (accent everywhere = no accent) | -1 | Code: accent color applied to majority of elements |

## Dimension 4: Motion Design (Weight: 15%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| No stagger on grouped elements (list/grid pops in simultaneously) | -4 | Code: multiple items use `delay: 0` or same delay |
| All springs use identical config (no variation) | -3 | Code: every spring call uses the same SPRING preset |
| No hold time — elements enter and scene immediately ends | -2 | Code: last animation ends within 10 frames of scene end |
| Linear interpolate used where spring would be better (entrances, scales) | -2 | Code: `interpolate()` for bounce-worthy motion (scale, entrance translate) |
| Memory anchor scene has same animation investment as other scenes | -2 | Code: anchor scene has equal or fewer spring/animation calls |
| Exit animation missing when scene needs one | -1 | Code: scene has enter but no exit when followed by hard cut |

## Dimension 5: Composition & Layout (Weight: 15%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| Text overflows viewport (extends beyond 1920x1080 bounds) | -4 | Screenshot: text clipped at edges |
| Everything dead-center with no spatial interest | -3 | Code: all elements use `alignItems: 'center'` + `justifyContent: 'center'` |
| No visual hierarchy — all elements same size/prominence | -3 | Screenshot: no clear primary element |
| Inconsistent margins/padding creating visual noise | -2 | Screenshot: uneven spacing between elements |
| Key content placed in bottom 10% (TV-unsafe zone) | -1 | Code: important text positioned at `top > 90%` or `bottom < 5%` |
| No breathing room — elements packed edge-to-edge | -1 | Screenshot: less than 40px margin from viewport edges |

## Dimension 6: Narrative Coherence (Weight: 10%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| Scene content doesn't match Phase 2 plan (wrong message) | -5 | Compare scene text content against plan table |
| Scene pattern doesn't match plan (e.g., plan says CardFlip, code does fade) | -3 | Compare animation pattern against plan table |
| Scene duration significantly differs from plan (> 30% off) | -2 | Compare `SCENE_FRAMES.sceneN` against planned duration |
| Tone mismatch — bouncy spring in a "professional" video or stiff spring in "playful" | -2 | Code: spring preset vs video's emotional tone from Phase 1 |
| Missing scene purpose — scene is decorative without content | -1 | Code: scene has animation but no meaningful text/content |

## Dimension 7: Technical Correctness (Weight: 10%)

Start at 10. Apply deductions:

| Deduction | Points | Detection Method |
|-----------|--------|-----------------|
| Remotion still render fails | -10 (instant-fail) | Still command exits non-zero |
| Scene not wired into Composition.tsx | -5 | Code: scene import/usage missing from Composition.tsx |
| Scenes in TransitionSeries lack own opaque background | -5 | Code: scenes rendered directly inside `TransitionSeries.Sequence` without `SceneWithBackground` wrapper. Causes transition overlap where both scenes are visible simultaneously during fade. |
| Scene not registered in Root.tsx as preview | -3 | Code: no `<Composition id="SceneN-Preview">` in Root.tsx |
| Hardcoded values instead of config.ts constants | -2 | Code: magic numbers for colors, sizes, frames instead of COLORS/TYPOGRAPHY/SCENE_FRAMES |
| Missing frame/fps hooks (static scene) | -2 | Code: no `useCurrentFrame()` or `useVideoConfig()` in scene |
| Unused imports | -1 | Code: imported modules not referenced |

---

## Auto-Fix Mapping

When a deduction is detected, apply the corresponding fix. Each fix is a specific code change — not a vague suggestion.

### Anti-Pattern Fixes

| Deduction | Fix |
|-----------|-----|
| Blacklisted display font | Replace `fontFamily` with the style preset's recommended font. E.g., Apple Minimal → `"Satoshi"`, Bold Typography → `"Clash Display"`, Dark Tech → `"Geist"` |
| Purple-to-blue gradient on white | Replace gradient with style preset's `gradientBlobA`/`gradientBlobB` colors, or switch to solid background |
| All elements same fade timing | Add staggered `delay` to spring calls: `delay: index * 4` for fast tone, `delay: index * 8` for slow tone |
| Pure white/black background no texture | Add FluidBackground component or NoiseOverlay at low opacity |
| Same entrance on all text | Differentiate: hero text uses `SPRING.bouncy` + `translateY`, body text uses `SPRING.smooth` + `opacity` only |
| Everything center-aligned | Move primary text to `left: '12%'` or `left: '15%'` with `textAlign: 'left'`; keep CTA centered |

### Typography Fixes

| Deduction | Fix |
|-----------|-----|
| Display/body ratio < 2x | Increase `heroSize` to at least `bodySize * 2.5` in config.ts |
| No weight contrast | Set display weight to 700-900, body weight to 400-500 |
| Line height too loose | Set display text `lineHeight: 0.9` (Bold Typography) or `lineHeight: 1.0` (other presets) |
| Missing font-weight | Add explicit `fontWeight: TYPOGRAPHY.weight.bold` to display, `fontWeight: 400` to body |
| Body text too large | Reduce body font-size to 28-32px range |
| Label same as body | Reduce label size to `bodySize * 0.6` |

### Color & Contrast Fixes

| Deduction | Fix |
|-----------|-----|
| Text unreadable | Add `textShadow: '0 2px 20px rgba(0,0,0,0.5)'` or place semi-transparent overlay behind text |
| No dominant accent | Pick one accent, relegate others to `textSecondary` or remove |
| Safe blue only | Replace with style preset's specified accent, or choose a bolder alternative |
| Text on gradient without aid | Add `background: 'rgba(0,0,0,0.3)'` panel behind text, or `textShadow` |
| Secondary text low contrast | Lighten on dark bg (`opacity: 0.7` → `0.85`) or darken on light bg |
| Accent overused | Limit accent to 1-2 elements; others use `textPrimary` or `textSecondary` |

### Motion Fixes

| Deduction | Fix |
|-----------|-----|
| No stagger on groups | Add `delay: index * N` where N = 3 (fast), 5 (medium), 8 (slow) based on tone |
| All springs identical config | Vary: hero entrance `SPRING.bouncy`, supporting elements `SPRING.smooth`, exits `SPRING.stiff` |
| No hold time | Extend scene frames by 15-25 frames, or add delay before exit starts |
| Linear interpolate for entrances | Replace `interpolate()` entrance with `spring({ frame, fps, config: SPRING.snappy })` |
| Anchor scene underinvested | Add secondary animation (highlight, scale pulse, or stagger) to memory anchor scene |
| Missing exit animation | Add opacity fade-out via `interpolate(frame, [exitStart, sceneEnd], [1, 0])` in last 15% of frames |

### Composition Fixes

| Deduction | Fix |
|-----------|-----|
| Text overflow | Reduce font size by 15% or add `maxWidth: '85%'` container |
| Dead-center everything | Shift primary element to `position: 'absolute', left: '12%', top: '35%'` |
| No visual hierarchy | Make hero text 2.5x body size; add opacity difference (hero: 1.0, supporting: 0.7) |
| Inconsistent spacing | Standardize: 48px between major elements, 24px between related elements |
| Content in unsafe zone | Move to `top: '15%'` minimum, `bottom: '15%'` minimum |
| No breathing room | Add `padding: '60px 80px'` to outermost content container |

### Narrative Fixes

| Deduction | Fix |
|-----------|-----|
| Wrong content | Replace scene text with the message from Phase 2 plan table |
| Wrong pattern | Rewrite scene animation to match planned pattern |
| Duration off by > 30% | Adjust `SCENE_FRAMES.sceneN` in config.ts to match plan |
| Tone mismatch | Replace spring config: Playful → `SPRING.wobbly`/`SPRING.pop`, Professional → `SPRING.smooth`/`SPRING.snappy` |
| No meaningful content | Add the planned text content; remove purely decorative animation |

### Technical Fixes

| Deduction | Fix |
|-----------|-----|
| Render fails | Read error output, fix syntax/import/type errors |
| Not in Composition.tsx | Add scene import and `<TransitionSeries.Sequence>` entry |
| Scenes lack own background in TransitionSeries | Wrap each scene with `<SceneWithBackground>` component that includes `backgroundColor` + `FluidBackground`. Remove any shared FluidBackground from outside TransitionSeries. See `project-scaffold.md` Composition.tsx template. |
| Not in Root.tsx | Add `<Composition id="SceneN-Preview">` registration |
| Hardcoded values | Replace with `COLORS.x`, `TYPOGRAPHY.x`, `SCENE_FRAMES.x` references |
| Missing frame hooks | Add `const frame = useCurrentFrame(); const { fps } = useVideoConfig();` |
| Unused imports | Remove unused import lines |

---

## Cross-Scene Tracking

Maintain a running context across all scenes within a single video production to enforce variety:

```
Scene Tracking Context:
├── Accent colors used per scene     → avoid same highlight color 3x in a row
├── Display fonts used               → should be consistent (same font, varied weight)
├── Spring presets used per scene     → avoid every scene using SPRING.bouncy
├── Entrance directions used         → rotate: left, right, bottom, scale, none
├── Stagger delays used              → vary between scenes (3f, 5f, 8f)
└── Techniques used per scene        → track for the evaluation summary
```

**Variety checks (applied at Scene 3+):**

| Check | Trigger | Recommendation |
|-------|---------|---------------|
| Same spring preset 3x in a row | Scene N, N-1, N-2 use identical SPRING.* | Switch to a contrasting preset for this scene |
| Same entrance direction 3x in a row | All recent scenes enter from same direction | Change entrance to opposite direction or use scale |
| No accent color variation | Same highlight/accent used on every scene | Introduce secondary accent from the style preset |

---

## Evaluation Report Template

After scoring each scene, output the report in this format:

```
┌─────────────────────────────────────────────────┐
│  SCENE EVALUATION: Scene {N} — {SceneName}      │
│  Iteration: {1|2|3}/3                            │
├──────────────────────┬──────────┬────────────────┤
│ Dimension            │ Score    │ Weight         │
├──────────────────────┼──────────┼────────────────┤
│ Anti-Pattern         │ {X}/10   │ 20%            │
│ Typography           │ {X}/10   │ 15%            │
│ Color & Contrast     │ {X}/10   │ 15%            │
│ Motion Design        │ {X}/10   │ 15%            │
│ Composition          │ {X}/10   │ 15%            │
│ Narrative Coherence  │ {X}/10   │ 10%            │
│ Technical            │ {X}/10   │ 10%            │
├──────────────────────┼──────────┼────────────────┤
│ WEIGHTED TOTAL       │ {X.X}    │                │
├──────────────────────┴──────────┴────────────────┤
│ Deductions:                                      │
│  - {dimension}: {deduction description} (-{N})   │
│  - {dimension}: {deduction description} (-{N})   │
├──────────────────────────────────────────────────┤
│ Verdict: {PASS | AUTO-FIX | WARNING}             │
│ {Fix actions if AUTO-FIX}                        │
└──────────────────────────────────────────────────┘
```

---

## Full Evaluation Summary Template

After all scenes pass evaluation, output a summary before Phase 5:

```
┌──────────────────────────────────────────────────────────┐
│              VIDEO EVALUATION SUMMARY                    │
├───────┬──────────────────┬─────────┬─────────────────────┤
│ Scene │ Name             │ Score   │ Iterations          │
├───────┼──────────────────┼─────────┼─────────────────────┤
│ 1     │ {SceneName}      │ {X.X}   │ {1|2|3}             │
│ 2     │ {SceneName}      │ {X.X}   │ {1|2|3}             │
│ ...   │ ...              │ ...     │ ...                 │
├───────┼──────────────────┼─────────┼─────────────────────┤
│ AVG   │                  │ {X.X}   │                     │
├───────┴──────────────────┴─────────┴─────────────────────┤
│ Cross-Scene Notes:                                       │
│  - Fonts: {font list}                                    │
│  - Accent colors: {colors used}                          │
│  - Spring presets: {presets per scene}                    │
│  - Entrance directions: {directions per scene}           │
│  - Warnings: {any scenes that passed with warnings}      │
├──────────────────────────────────────────────────────────┤
│ Ready for Phase 5: Rendering                             │
└──────────────────────────────────────────────────────────┘
```
