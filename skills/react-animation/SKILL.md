---
name: react-animation
description: ReactBits animations for Remotion - curated for aesthetic excellence in video production
metadata:
  tags: react-animation, reactbits, remotion, animation, video, effects, text, backgrounds, motion-graphics
---

## When to use

Use this skill when creating Remotion video compositions that need **aesthetically refined** visual effects. Components are curated for motion graphics excellence, categorized by visual style.

## Installation

```bash
npx shadcn@latest add https://reactbits.dev/r/<Component>-TS-CSS
```

---

## 🎨 Aesthetic Categories

Components organized by visual style. **Avoid mixing more than 2 styles in one video.**

---

## 1. Elegant & Soft (优雅柔和)

*Smooth, cinematic, refined. Best for luxury brands, emotional storytelling.*

### Text
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **BlurText** | `npx shadcn add https://reactbits.dev/r/BlurText-TS-CSS` | Blur-to-clear cinematic reveal |

### Backgrounds
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **Aurora** | `npx shadcn add https://reactbits.dev/r/Aurora-TS-CSS` | Flowing northern lights |
| **Silk** | `npx shadcn add https://reactbits.dev/r/Silk-TS-CSS` | Minimalist fabric waves |
| **Grainient** | `npx shadcn add https://reactbits.dev/r/Grainient-TS-CSS` | Grainy artistic gradients |

### Effects
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **Ribbons** | `npx shadcn add https://reactbits.dev/r/Ribbons-TS-CSS` | Flowing silk ribbons |
| **ShapeBlur** | `npx shadcn add https://reactbits.dev/r/ShapeBlur-TS-CSS` | Soft abstract geometry |

**Usage Pattern:**
```tsx
const ElegantScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  return (
    <AbsoluteFill>
      <Aurora time={frame / fps} colorStops={['#3A29FF', '#FF94B4', '#FF3232']} />
      <BlurText text="Elegant Title" startFrame={15} />
    </AbsoluteFill>
  );
};
```

---

## 2. Modern & Tech (现代科技)

*Cutting-edge, dynamic, futuristic. Best for tech products, startups, innovation.*

### Text
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **GlitchText** | `npx shadcn add https://reactbits.dev/r/GlitchText-TS-CSS` | Digital glitch artifacts |
| **GradientText** | `npx shadcn add https://reactbits.dev/r/GradientText-TS-CSS` | Flowing gradient sweep |

### Backgrounds
| Component | Install | Aesthetic | Disable Mouse |
|-----------|---------|-----------|---------------|
| **Iridescence** | `npx shadcn add https://reactbits.dev/r/Iridescence-TS-CSS` | Rainbow oil-slick | `mouseReact={false}` |
| **LiquidChrome** | `npx shadcn add https://reactbits.dev/r/LiquidChrome-TS-CSS` | Liquid metal surface | `interactive={false}` |
| **Particles** | `npx shadcn add https://reactbits.dev/r/Particles-TS-CSS` | Floating data points | `moveParticlesOnHover={false}` |

### Effects
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **MetaBalls** | `npx shadcn add https://reactbits.dev/r/MetaBalls-TS-CSS` | Organic liquid fusion |
| **Antigravity** | `npx shadcn add https://reactbits.dev/r/Antigravity-TS-CSS` | Ethereal particle field |

**Usage Pattern:**
```tsx
const TechScene: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Iridescence mouseReact={false} color={[0.3, 0.1, 0.8]} speed={1} />
    <GlitchText speed={0.5} enableShadows enableOnHover={false}>
      FUTURE IS NOW
    </GlitchText>
  </AbsoluteFill>
);
```

---

## 3. Luxury & Premium (奢华高端)

*Metallic, refined, sophisticated. Best for luxury goods, finance, high-end services.*

### Text
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **ShinyText** | `npx shadcn add https://reactbits.dev/r/ShinyText-TS-CSS` | Metallic sheen sweep |

### Backgrounds
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **Silk** | `npx shadcn add https://reactbits.dev/r/Silk-TS-CSS` | Premium fabric texture |

### Effects
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **StarBorder** | `npx shadcn add https://reactbits.dev/r/StarBorder-TS-CSS` | Animated gradient border |

**Usage Pattern:**
```tsx
const LuxuryScene: React.FC = () => (
  <AbsoluteFill style={{ background: '#0a0a0a' }}>
    <Silk speed={0.5} color="#1a1a2e" />
    <StarBorder color="#gold" speed="4s">
      <ShinyText text="PREMIUM" color="#c9b037" shineColor="#fff" />
    </StarBorder>
  </AbsoluteFill>
);
```

---

## 4. Retro & Pixel (复古像素)

*Nostalgic, digital, lo-fi. Best for gaming, retro tech, vaporwave aesthetics.*

### Text
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **TextType** | `npx shadcn add https://reactbits.dev/r/TextType-TS-CSS` | Terminal typewriter |
| **DecryptedText** | `npx shadcn add https://reactbits.dev/r/DecryptedText-TS-CSS` | Data decryption effect |

### Transitions
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **PixelTransition** | `npx shadcn add https://reactbits.dev/r/PixelTransition-TS-CSS` | Pixel grid dissolve |

### Backgrounds
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **LetterGlitch** | `npx shadcn add https://reactbits.dev/r/LetterGlitch-TS-CSS` | Matrix code rain |
| **Dither** | `npx shadcn add https://reactbits.dev/r/Dither-TS-CSS` | Retro dithering |
| **FaultyTerminal** | `npx shadcn add https://reactbits.dev/r/FaultyTerminal-TS-CSS` | CRT monitor effect |

**Usage Pattern:**
```tsx
const RetroScene: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <LetterGlitch glitchSpeed={100} glitchColors={['#0f0', '#00ff41']} />
    <GlitchText>SYSTEM OVERRIDE</GlitchText>
  </AbsoluteFill>
);
```

---

## 5. Energy & Dramatic (能量戏剧)

*High-impact, dynamic, powerful. Best for action, sports, announcements.*

### Backgrounds
| Component | Install | Aesthetic | Disable Mouse |
|-----------|---------|-----------|---------------|
| **Lightning** | `npx shadcn add https://reactbits.dev/r/Lightning-TS-CSS` | Electric storm | None |
| **Beams** | `npx shadcn add https://reactbits.dev/r/Beams-TS-CSS` | Volumetric light columns | None |
| **LightRays** | `npx shadcn add https://reactbits.dev/r/LightRays-TS-CSS` | God rays, dramatic | `followMouse={false}` |

**Usage Pattern:**
```tsx
const DramaticScene: React.FC = () => (
  <AbsoluteFill>
    <Lightning hue={45} intensity={0.8} speed={2} />
    <BlurText text="THUNDER STRIKE" />
  </AbsoluteFill>
);
```

---

## 6. Abstract & Artistic (抽象艺术)

*Experimental, artistic, unique. Best for creative projects, music videos.*

### Text
| Component | Install | Aesthetic |
|-----------|---------|-----------|
| **DecryptedText** | `npx shadcn add https://reactbits.dev/r/DecryptedText-TS-CSS` | Cryptic reveal |

### Backgrounds
| Component | Install | Aesthetic | Disable Mouse |
|-----------|---------|-----------|---------------|
| **Plasma** | `npx shadcn add https://reactbits.dev/r/Plasma-TS-CSS` | Organic flowing colors | `mouseInteractive={false}` |
| **Prism** | `npx shadcn add https://reactbits.dev/r/Prism-TS-CSS` | Light refraction | `animationType='rotate'` |

---

## 7. Utility (通用工具)

*Enhance any scene.*

### Overlay
| Component | Install | Purpose |
|-----------|---------|---------|
| **Noise** | `npx shadcn add https://reactbits.dev/r/Noise-TS-CSS` | Film grain texture overlay |

**Usage Pattern:**
```tsx
const SceneWithGrain: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    const ctx = canvasRef.current?.getContext('2d');
    if (!ctx || frame % 2 !== 0) return;
    
    const imageData = ctx.createImageData(width, height);
    for (let i = 0; i < imageData.data.length; i += 4) {
      const seed = frame * 100000 + i / 4;
      const val = Math.floor((Math.sin(seed) * 10000 % 1) * 255);
      imageData.data[i] = imageData.data[i + 1] = imageData.data[i + 2] = val;
      imageData.data[i + 3] = 15;
    }
    ctx.putImageData(imageData, 0, 0);
  }, [frame]);
  
  return (
    <>
      <YourScene />
      <canvas ref={canvasRef} style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }} />
    </>
  );
};
```

---

## 🔧 Core Adaptation Patterns

### Frame-Based Animation
Replace all time-driven animations with `useCurrentFrame()`:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';

// Before: time accumulation
// After: deterministic from frame
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const progress = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.out(Easing.cubic),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

### Seeded Randomness
Ensure deterministic rendering:

```tsx
function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

const rand = seededRandom(frame * 1000 + index);
```

### Shader Uniforms
For WebGL/OGL components:

```tsx
// Time uniform
uniforms.iTime.value = frame / fps;

// Scripted mouse path (optional)
uniforms.iMouse.value.set(
  0.5 + 0.3 * Math.sin(frame / fps),
  0.5 + 0.2 * Math.cos(frame / fps * 0.7)
);
```

---

## ⚠️ Style Consistency Guidelines

**DO:**
- ✅ Mix Elegant + Luxury styles (BlurText + ShinyText + Silk)
- ✅ Mix Modern + Retro styles (GlitchText + LetterGlitch)
- ✅ Use Noise overlay on ANY scene
- ✅ Keep backgrounds subtle when text is prominent

**DON'T:**
- ❌ Mix Elegant + Retro (BlurText + PixelTransition)
- ❌ Mix Luxury + Glitch (ShinyText + GlitchText)
- ❌ Use Lightning with complex text animations
- ❌ Use more than 2 background effects simultaneously

---

## 📦 Full Component List (35 curated)

### Text (6)
BlurText, GlitchText, GradientText, ShinyText, DecryptedText, TextType

### Backgrounds (18)
Aurora, Silk, Grainient, Lightning, Iridescence, LiquidChrome, Particles, Galaxy, Plasma, LetterGlitch, Beams, LightRays, Dither, FaultyTerminal, DarkVeil, PixelSnow, Balatro, Prism

### Effects (10)
MetaBalls, Ribbons, ShapeBlur, Antigravity, StarBorder, PixelTransition

### Utility (1)
Noise

---

## ❌ Removed Components

**Why these were removed:**

- **Low aesthetic value**: SplitText, FadeContent, AnimatedContent
- **Style overlap**: ElectricBorder (covered by GlitchText), Orb (covered by Iridescence)
- **Outdated aesthetics**: Hyperspeed, Cubes, Squares
- **Narrow use cases**: CircularText, RotatingText, TrueFocus
- **Functional > Aesthetic**: Counter, Stepper, Carousel (UI components)

---

## 🎬 Recommended Combinations

| Project Type | Text | Background | Effect | Mood |
|--------------|------|------------|--------|------|
| Luxury Brand | ShinyText | Silk | StarBorder | Premium |
| Tech Startup | GradientText | Iridescence | - | Innovative |
| Creative Studio | BlurText | Aurora | Ribbons | Artistic |
| Gaming | GlitchText | LetterGlitch | PixelTransition | Edgy |
| Documentary | BlurText | Grainient | Noise | Cinematic |
| Event Promo | DecryptedText | Lightning | - | Energetic |
