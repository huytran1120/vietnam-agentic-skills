---
name: p5js
description: "Generative visuals, algorithmic art, and creative coding with p5.js. Covers setup/draw life cycle, vector math (p5.Vector), Perlin noise, trigonometric wave synthesis, flow fields, cellular automata, generative typography, procedural textures, WebGL 3D mode in p5, instance mode encapsulation for React/Vue, and lossless video/canvas recording (saveCanvas, WebM/GIF)."
category: creative
risk: safe
source: community
source_repo: "processing/p5.js"
author: "processing"
tags: ["p5js", "creative-coding", "generative-art", "canvas", "algorithmic-art", "perlin-noise", "visuals", "processing"]
date_added: "2026-10-27"
---

# p5.js — Generative Art & Creative Coding Engine

p5.js is a creative coding library built on HTML5 Canvas and WebGL, designed for artists, designers, and developers to write algorithmic visuals, mathematical animations, and generative interaction systems.

---

## 1. Instance Mode (Clean Integration with Modern Frameworks)

Never use global mode in production applications or React/Next.js components. Always use **Instance Mode** to prevent polluting `window` and ensure clean lifecycle disposal:

```typescript
import p5 from 'p5';

export function mountP5Sketch(container: HTMLElement) {
  const sketch = (p: p5) => {
    let angle = 0;

    p.setup = () => {
      const canvas = p.createCanvas(container.clientWidth, container.clientHeight);
      p.frameRate(60);
      p.pixelDensity(Math.min(window.devicePixelRatio, 2));
      p.noStroke();
    };

    p.draw = () => {
      p.background(15, 23, 42, 25); // Subtle alpha trails

      p.translate(p.width / 2, p.height / 2);
      p.rotate(angle);

      for (let i = 0; i < 8; i++) {
        p.push();
        p.rotate((p.TWO_PI / 8) * i);
        p.fill(56, 189, 248, 180);
        p.circle(120, 0, 24 + p.sin(angle * 2 + i) * 10);
        p.pop();
      }

      angle += 0.02;
    };

    p.windowResized = () => {
      p.resizeCanvas(container.clientWidth, container.clientHeight);
    };
  };

  const instance = new p5(sketch, container);
  return () => instance.remove(); // Cleanup function
}
```

---

## 2. Advanced Flow Fields with Perlin Noise

```typescript
import p5 from 'p5';

export const flowFieldSketch = (p: p5) => {
  const scale = 20;
  let cols: number, rows: number;
  let zoff = 0;
  const particles: Particle[] = [];
  const numParticles = 800;

  class Particle {
    pos: p5.Vector;
    vel: p5.Vector;
    acc: p5.Vector;
    maxSpeed: number;
    prevPos: p5.Vector;

    constructor() {
      this.pos = p.createVector(p.random(p.width), p.random(p.height));
      this.vel = p.createVector(0, 0);
      this.acc = p.createVector(0, 0);
      this.maxSpeed = 2.5;
      this.prevPos = this.pos.copy();
    }

    update() {
      this.vel.add(this.acc);
      this.vel.limit(this.maxSpeed);
      this.pos.add(this.vel);
      this.acc.mult(0);
    }

    applyForce(force: p5.Vector) {
      this.acc.add(force);
    }

    show() {
      p.stroke(99, 102, 241, 40);
      p.strokeWeight(1.2);
      p.line(this.pos.x, this.pos.y, this.prevPos.x, this.prevPos.y);
      this.updatePrev();
    }

    updatePrev() {
      this.prevPos.x = this.pos.x;
      this.prevPos.y = this.pos.y;
    }

    edges() {
      if (this.pos.x > p.width) { this.pos.x = 0; this.updatePrev(); }
      if (this.pos.x < 0) { this.pos.x = p.width; this.updatePrev(); }
      if (this.pos.y > p.height) { this.pos.y = 0; this.updatePrev(); }
      if (this.pos.y < 0) { this.pos.y = p.height; this.updatePrev(); }
    }
  }

  p.setup = () => {
    p.createCanvas(800, 800);
    cols = p.floor(p.width / scale);
    rows = p.floor(p.height / scale);
    p.background(10, 10, 15);
    for (let i = 0; i < numParticles; i++) {
      particles.push(new Particle());
    }
  };

  p.draw = () => {
    let yoff = 0;
    const flowfield: p5.Vector[] = new Array(cols * rows);

    for (let y = 0; y < rows; y++) {
      let xoff = 0;
      for (let x = 0; x < cols; x++) {
        const index = x + y * cols;
        const angle = p.noise(xoff, yoff, zoff) * p.TWO_PI * 3;
        const v = p5.Vector.fromAngle(angle);
        v.setMag(0.8);
        flowfield[index] = v;
        xoff += 0.08;
      }
      yoff += 0.08;
    }
    zoff += 0.003;

    for (const particle of particles) {
      const x = p.floor(particle.pos.x / scale);
      const y = p.floor(particle.pos.y / scale);
      const index = x + y * cols;
      const force = flowfield[index];
      if (force) particle.applyForce(force);
      particle.update();
      particle.edges();
      particle.show();
    }
  };
};
```

---

## 3. High-Res Export for Video & Print

```typescript
// Save high-resolution PNG for posters / prints
p.keyPressed = () => {
  if (p.key === 's') {
    p.saveCanvas('generative-artwork-' + Date.now(), 'png');
  }
};

// Deterministic random seed for reproducible renders
export function setReproducibleSeed(p: p5, seed: number) {
  p.randomSeed(seed);
  p.noiseSeed(seed);
}
```

---

## 4. Best Practices & Performance Checklist

- **Minimize Memory Allocations in `draw()`**: Avoid calling `p.createVector()` inside loops executed 60 times a second. Re-use vector instances with `.set(x, y)` to prevent garbage collection hiccups.
- **Use `noLoop()` When Static**: If generating generative static art, call `p.noLoop()` at the end of `setup()` so the CPU doesn't spin unnecessarily.
- **Always Pair `push()` with `pop()`**: Enclose coordinate modifications (`translate`, `rotate`, `scale`) and styling overrides (`fill`, `stroke`) between `p.push()` and `p.pop()`.
- **Prefer WebGL Mode (`p.WEBGL`) for 3D Math**: When rendering 3D geometries, meshes, or custom shaders, initialize `p.createCanvas(w, h, p.WEBGL)`. Note that coordinates in WEBGL mode originate at `(0, 0)` in the canvas center instead of top-left.
