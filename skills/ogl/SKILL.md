---
name: ogl
description: "Minimal, lightweight WebGL library (~10KB gzipped) by oframe for high-performance custom GLSL shaders, fullscreen post-processing, particles, and low-level WebGL graphics. Covers Renderer, Camera, Transform, Program (GLSL uniform and attribute binding), Mesh, Geometry, Texture, RenderTarget, Post post-processing pipelines, instanced rendering, and zero-overhead GPU computing."
category: graphics-processing
risk: safe
source: community
source_repo: "oframe/ogl"
author: "oframe"
tags: ["ogl", "webgl", "custom-shaders", "glsl", "post-processing", "minimal-webgl", "render-targets", "graphics-processing"]
date_added: "2026-10-27"
---

# OGL — Minimal, High-Performance WebGL Library

OGL is an ultra-lightweight WebGL library (~10KB gzipped) developed by oframe for developers who want direct, unbloated control over WebGL pipelines, custom GLSL shaders, fullscreen post-processing effects, and instanced particles without the overhead of Three.js.

---

## 1. Minimal OGL Pipeline Setup

```typescript
import { Renderer, Camera, Transform, Program, Mesh, Box } from 'ogl';

export function createOGLScene(container: HTMLElement) {
  // 1. Initialize renderer
  const renderer = new Renderer({ dpr: Math.min(window.devicePixelRatio, 2), alpha: true });
  const gl = renderer.gl;
  container.appendChild(gl.canvas);

  // 2. Camera & Scene graph
  const camera = new Camera(gl, { fov: 35 });
  camera.position.set(0, 1, 5);
  camera.lookAt([0, 0, 0]);

  const scene = new Transform();

  // 3. Geometry & Custom GLSL Shader Program
  const geometry = new Box(gl);

  const program = new Program(gl, {
    vertex: /* glsl */ `
      attribute vec3 position;
      attribute vec3 normal;

      uniform mat4 modelViewMatrix;
      uniform mat4 projectionMatrix;
      uniform mat3 normalMatrix;

      varying vec3 vNormal;

      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragment: /* glsl */ `
      precision highp float;
      varying vec3 vNormal;
      uniform float uTime;

      void main() {
        vec3 light = normalize(vec3(0.5, 1.0, 0.3));
        float d = max(0.0, dot(vNormal, light));
        vec3 color = mix(vec3(0.1, 0.4, 0.9), vec3(0.9, 0.2, 0.5), sin(uTime + vNormal.y * 3.0) * 0.5 + 0.5);
        gl_FragColor = vec4(color * (d * 0.8 + 0.2), 1.0);
      }
    `,
    uniforms: {
      uTime: { value: 0 },
    },
  });

  const mesh = new Mesh(gl, { geometry, program });
  mesh.setParent(scene);

  // Resize handler
  function resize() {
    renderer.setSize(container.clientWidth, container.clientHeight);
    camera.perspective({ aspect: gl.canvas.width / gl.canvas.height });
  }
  window.addEventListener('resize', resize);
  resize();

  // Animation render loop
  let animationFrameId: number;
  function update(timeMs: number) {
    animationFrameId = requestAnimationFrame(update);
    const time = timeMs * 0.001;

    mesh.rotation.y = time * 0.5;
    mesh.rotation.x = time * 0.3;
    program.uniforms.uTime.value = time;

    renderer.render({ scene, camera });
  }
  animationFrameId = requestAnimationFrame(update);

  return () => {
    cancelAnimationFrame(animationFrameId);
    window.removeEventListener('resize', resize);
    gl.canvas.remove();
  };
}
```

---

## 2. Fullscreen Post-Processing Pipeline (`Post`)

OGL features an elegant `Post` pass orchestrator for blooming, chromatic aberration, blurring, and custom distortion shaders:

```typescript
import { Renderer, Camera, Transform, Post, Program } from 'ogl';

export function setupPostProcessing(renderer: Renderer) {
  const gl = renderer.gl;
  const post = new Post(gl);

  // Add custom distortion pass
  const wavePass = post.addPass({
    fragment: /* glsl */ `
      precision highp float;
      uniform sampler2D tMap;
      uniform float uTime;
      varying vec2 vUv;

      void main() {
        vec2 uv = vUv;
        uv.x += sin(uv.y * 20.0 + uTime * 4.0) * 0.008;
        gl_FragColor = texture2D(tMap, uv);
      }
    `,
    uniforms: {
      uTime: { value: 0 },
    },
  });

  return { post, wavePass };
}
```

---

## 3. Instanced Particle Geometry (100,000+ Particles)

```typescript
import { Geometry, Program, Mesh, Renderer } from 'ogl';

export function createInstancedParticles(gl: WebGLRenderingContext, count: number) {
  // Base triangle geometry
  const geometry = new Geometry(gl, {
    position: { size: 3, data: new Float32Array([-0.05, -0.05, 0, 0.05, -0.05, 0, 0, 0.05, 0]) },
  });

  // Instanced attribute buffers
  const offsetData = new Float32Array(count * 3);
  const randomData = new Float32Array(count * 4);

  for (let i = 0; i < count; i++) {
    offsetData[i * 3 + 0] = (Math.random() - 0.5) * 10;
    offsetData[i * 3 + 1] = (Math.random() - 0.5) * 10;
    offsetData[i * 3 + 2] = (Math.random() - 0.5) * 10;

    randomData[i * 4 + 0] = Math.random();
    randomData[i * 4 + 1] = Math.random();
    randomData[i * 4 + 2] = Math.random();
    randomData[i * 4 + 3] = Math.random();
  }

  geometry.addAttribute('offset', { instanced: 1, size: 3, data: offsetData });
  geometry.addAttribute('random', { instanced: 1, size: 4, data: randomData });

  const program = new Program(gl, {
    vertex: /* glsl */ `
      attribute vec3 position;
      attribute vec3 offset;
      attribute vec4 random;
      uniform mat4 modelViewMatrix;
      uniform mat4 projectionMatrix;
      uniform float uTime;

      void main() {
        vec3 pos = position + offset;
        pos.y += sin(uTime + random.x * 6.28) * 0.5;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragment: /* glsl */ `
      precision highp float;
      void main() {
        gl_FragColor = vec4(0.2, 0.8, 1.0, 0.9);
      }
    `,
    uniforms: { uTime: { value: 0 } },
    transparent: true,
  });

  return new Mesh(gl, { geometry, program });
}
```

---

## 4. Critical Rules & Performance Checklist

- **Manage Uniform Value Updates In-Place**: Do not recreate uniform objects on each frame. Update primitive values directly: `program.uniforms.uTime.value = time`.
- **Pre-multiply Alpha in Textures When Blending**: When loading PNG assets, specify `premultiplyAlpha: true` in `Texture(gl, { ... })` to avoid dark fringing on transparent edges.
- **Dispose Buffers on Scene Destruction**: Call `geometry.remove()` and delete WebGL textures when tearing down canvases to prevent GPU resource leaks.
