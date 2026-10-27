---
name: tsparticles
description: "Lightweight, highly customizable particle animations, interactive canvas backgrounds, confetti, and visual effects with tsParticles. Covers Engine architecture (init, load, presets), interactive modes (hover repulse/grab/bubble, click push), physics trails, polygon masks, confetti bursts, custom shapes, React/Vue integration (@tsparticles/react), and battery/GPU performance optimization."
category: frontend
risk: safe
source: community
source_repo: "tsparticles/tsparticles"
author: "tsparticles"
tags: ["tsparticles", "particle-effects", "confetti", "interactive-particles", "canvas-background", "react-tsparticles", "web-animation", "frontend"]
date_added: "2026-10-27"
---

# tsParticles — Interactive Particle & Confetti Engine

`tsParticles` is a TypeScript library for building interactive particle effects, animated background canvases, floating nodes, constellations, snow, fireworks, and confetti explosions.

---

## 1. Quickstart: Clean Web / TypeScript Initialization

```typescript
import { tsParticles } from '@tsparticles/engine';
import { loadSlim } from '@tsparticles/slim';

export async function initParticles(containerId: string) {
  // Use slim package to minimize bundle weight
  await loadSlim(tsParticles);

  await tsParticles.load({
    id: containerId,
    options: {
      background: {
        color: { value: '#0f172a' },
      },
      fpsLimit: 60,
      interactivity: {
        events: {
          onHover: { enable: true, mode: 'grab' },
          onClick: { enable: true, mode: 'push' },
          resize: { enable: true },
        },
        modes: {
          grab: { distance: 180, links: { opacity: 0.8, color: '#38bdf8' } },
          push: { quantity: 4 },
        },
      },
      particles: {
        color: { value: '#94a3b8' },
        links: {
          color: '#475569',
          distance: 140,
          enable: true,
          opacity: 0.4,
          width: 1,
        },
        move: {
          enable: true,
          speed: 1.5,
          direction: 'none',
          outModes: { default: 'bounce' },
        },
        number: {
          density: { enable: true },
          value: 80,
        },
        opacity: { value: 0.6 },
        shape: { type: 'circle' },
        size: { value: { min: 1, max: 3 } },
      },
      detectRetina: true,
    },
  });
}
```

---

## 2. Declarative React Integration (`@tsparticles/react`)

```tsx
import React, { useEffect, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadBasic } from '@tsparticles/basic';
import type { Container } from '@tsparticles/engine';

export const InteractiveParticlesBackground: React.FC = () => {
  const [init, setInit] = useState(false);

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadBasic(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);

  const particlesLoaded = async (container?: Container): Promise<void> => {
    console.log('Particles engine ready', container?.id);
  };

  if (!init) return null;

  return (
    <Particles
      id="tsparticles"
      particlesLoaded={particlesLoaded}
      options={{
        particles: {
          number: { value: 50 },
          move: { enable: true, speed: 2 },
          color: { value: '#818cf8' },
          size: { value: { min: 2, max: 4 } },
        },
      }}
      className="absolute inset-0 pointer-events-none"
    />
  );
};
```

---

## 3. High-Impact Confetti Cannon

```typescript
import { confetti } from '@tsparticles/confetti';

export function fireCelebrationConfetti() {
  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 },
    colors: ['#38bdf8', '#818cf8', '#f472b6', '#facc15'],
    disableForReducedMotion: true,
  });
}
```

---

## 4. Best Practices & Performance Optimization

- **Prefer `@tsparticles/slim` Over the Full Package**: Never import the massive monolithic bundle in production. Use `@tsparticles/slim` or `@tsparticles/basic` to reduce JS payload by over 70%.
- **Set `fpsLimit: 60`**: Avoid unconstrained refresh rates on 144Hz-240Hz gaming monitors which drain mobile laptop batteries.
- **Respect `prefers-reduced-motion`**: Include `disableForReducedMotion: true` in your configurations to adhere to accessibility standards.
- **Use `detectRetina: true` with Caution**: On 4K monitors, high particle counts multiplied by devicePixelRatio can induce lag. Keep particle counts under 120 for linked nodes.
