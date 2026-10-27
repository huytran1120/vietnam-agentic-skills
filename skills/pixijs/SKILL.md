---
name: pixijs
description: "High-performance 2D WebGL/WebGPU graphics rendering with PixiJS (v8+). Covers Application setup, Scene Graph (Container, Sprite, Graphics, Text, Mesh), Assets loading, Ticker animation loops, custom GLSL filters/shaders, particle systems, sprite sheets/atlases, blend modes, batching, draw call minimization, and interactive pointer events for web, games, and creative coding."
category: graphics-processing
risk: safe
source: community
source_repo: "pixijs/pixijs"
author: "pixijs"
tags: ["pixijs", "webgl", "webgpu", "2d-engine", "canvas-rendering", "sprites", "shaders", "graphics-processing", "creative-coding"]
date_added: "2026-10-27"
---

# PixiJS — High-Performance 2D WebGL & WebGPU Engine

PixiJS is the industry standard for hardware-accelerated 2D graphics on the web. It renders using WebGPU with automated WebGL fallback, providing 60-120fps performance for thousands of animated sprites, interactive data visualizations, and creative coding effects.

---

## 1. PixiJS v8 Architecture & Mental Model

```
+-------------------------------------------------------------+
|                      PixiJS Application                     |
|  (Renderer [WebGPU/WebGL] + Stage [Root Container] + Ticker) |
+-------------------------------------------------------------+
                               |
               +---------------+---------------+
               |                               |
       [Container: Scene]             [Container: UI Layer]
         |            |                        |
     [Sprite]     [Graphics]                [Text]
         |            |                        |
     (Texture)    (Vector Paths)           (Bitmap/Canvas)
```

- **Application**: The orchestrator holding the Canvas element, Renderer, Root Stage Container, and Ticker.
- **Scene Graph**: Hierarchical tree of `Container` instances. Transforming a parent automatically transforms all children.
- **Automatic Batching**: Sprites sharing the same base texture are batched into a single GPU draw call.
- **Assets API**: Promise-based asset manager with caching, format detection (WebP, AVIF), and texture atlases.

---

## 2. Quickstart: App Initialization & Asset Loading

```typescript
import { Application, Assets, Sprite, Container } from 'pixi.js';

async function initCanvas() {
  const app = new Application();

  // Initialize renderer with WebGPU (auto fallback to WebGL)
  await app.init({
    width: 1280,
    height: 720,
    backgroundColor: 0x0f172a,
    resolution: Math.min(window.devicePixelRatio, 2),
    autoDensity: true,
    antialias: true,
  });

  document.body.appendChild(app.canvas);

  // Load texture atlas or individual images
  const texture = await Assets.load('https://pixijs.com/assets/bunny.png');

  const sprite = new Sprite(texture);
  sprite.anchor.set(0.5); // Center origin
  sprite.x = app.screen.width / 2;
  sprite.y = app.screen.height / 2;
  sprite.scale.set(2);

  app.stage.addChild(sprite);

  // Ticker loop (delta time adjusted)
  app.ticker.add((time) => {
    sprite.rotation += 0.02 * time.deltaTime;
  });
}
```

---

## 3. High-Performance Vector Graphics & Dynamic Paths

```typescript
import { Graphics } from 'pixi.js';

export function createProceduralChart(width: number, height: number): Graphics {
  const g = new Graphics();

  // Background grid
  g.rect(0, 0, width, height)
   .fill({ color: 0x1e293b, alpha: 0.8 })
   .stroke({ width: 1, color: 0x334155 });

  // Smooth wave graph
  g.moveTo(0, height * 0.7);
  for (let x = 0; x <= width; x += 20) {
    const y = height * 0.5 + Math.sin(x * 0.02) * 60 + Math.cos(x * 0.05) * 30;
    g.lineTo(x, y);
  }

  // Neon glowing stroke
  g.stroke({
    width: 3,
    color: 0x38bdf8,
    cap: 'round',
    join: 'round',
  });

  return g;
}
```

---

## 4. Custom GLSL Filter / Shaders

```typescript
import { Filter, GlProgram } from 'pixi.js';

const vertexShader = `
  in vec2 aPosition;
  out vec2 vTextureCoord;

  uniform vec4 uInputSize;
  uniform vec4 uOutputFrame;

  vec4 filterVertexPosition(void) {
    vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;
    position.x = position.x * (2.0 / uInputSize.x) - 1.0;
    position.y = position.y * (2.0 / uInputSize.y) - 1.0;
    return vec4(position, 0.0, 1.0);
  }

  void main(void) {
    gl_Position = filterVertexPosition();
    vTextureCoord = aPosition;
  }
`;

const fragmentShader = `
  in vec2 vTextureCoord;
  out vec4 finalColor;

  uniform sampler2D uTexture;
  uniform float uTime;
  uniform vec2 uResolution;

  void main() {
    vec2 uv = vTextureCoord;
    // Chromatic aberration wave
    float r = texture(uTexture, uv + vec2(sin(uTime * 2.0 + uv.y * 10.0) * 0.005, 0.0)).r;
    float g = texture(uTexture, uv).g;
    float b = texture(uTexture, uv - vec2(cos(uTime * 2.0 + uv.x * 10.0) * 0.005, 0.0)).b;
    finalColor = vec4(r, g, b, 1.0);
  }
`;

export function createChromaticAberrationFilter(): Filter {
  const glProgram = GlProgram.from({
    vertex: vertexShader,
    fragment: fragmentShader,
  });

  const filter = new Filter({
    glProgram,
    resources: {
      uniforms: {
        uTime: { value: 0.0, type: 'f32' },
      },
    },
  });

  return filter;
}
```

---

## 5. 10,000+ Particles & Batch Optimization

```typescript
import { Container, Sprite, Texture, Assets } from 'pixi.js';

export async function createParticleStorm(count: number, width: number, height: number) {
  const texture = await Assets.load('/assets/glow-particle.png');
  const container = new Container();

  const particles: Array<{
    sprite: Sprite;
    vx: number;
    vy: number;
  }> = [];

  for (let i = 0; i < count; i++) {
    const sprite = new Sprite(texture);
    sprite.x = Math.random() * width;
    sprite.y = Math.random() * height;
    sprite.anchor.set(0.5);
    sprite.scale.set(Math.random() * 0.5 + 0.2);
    sprite.alpha = Math.random() * 0.7 + 0.3;

    container.addChild(sprite);
    particles.push({
      sprite,
      vx: (Math.random() - 0.5) * 2,
      vy: Math.random() * 2 + 1,
    });
  }

  function update() {
    for (let i = 0; i < count; i++) {
      const p = particles[i];
      p.sprite.y += p.vy;
      p.sprite.x += p.vx;
      if (p.sprite.y > height) p.sprite.y = 0;
      if (p.sprite.x > width) p.sprite.x = 0;
      if (p.sprite.x < 0) p.sprite.x = width;
    }
  }

  return { container, update };
}
```

---

## 6. Critical Rules & Performance Checklist

- **Use Texture Atlases**: Always pack multiple UI icons/sprites into spritesheets (`.json` generated by TexturePacker) to ensure single draw-call batching.
- **Set `interactiveChildren = false`**: On containers with non-interactive decorative elements, disable event bubbling to save CPU hit-test cycles.
- **Destroy Unused Textures**: Call `texture.destroy(true)` and `container.destroy({ children: true })` on component unmount to prevent GPU VRAM leaks.
- **Cap Device Pixel Ratio**: Never use raw `window.devicePixelRatio` unconditionally on 4K/Retina displays (can exceed 3x-4x, blowing GPU fillrate). Always use `Math.min(window.devicePixelRatio, 2)`.
