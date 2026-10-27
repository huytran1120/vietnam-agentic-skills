---
name: gl-transitions
description: "Open-source GLSL shader transitions for web video, HTML5 Canvas, Remotion (@remotion/gl-transitions), and creative coding. Covers standard GLSL transition signature (vec4 transition(vec2 uv)), texture sampling (getFromColor, getToColor, progress, ratio), custom uniform parameters, 50+ transition types (crossfade, wipe, cube, directional warp, ripple, kaleidoscope, glitch, morph), and WebGL render pipelines."
category: graphics-processing
risk: safe
source: community
source_repo: "gl-transitions/gl-transitions"
author: "gl-transitions"
tags: ["gl-transitions", "glsl", "shaders", "video-transitions", "webgl", "remotion-transitions", "canvas-transitions", "graphics-processing"]
date_added: "2026-10-27"
---

# GL Transitions — Shader-Based Video & Image Transitions

`gl-transitions` is an open-source standard and collection of GLSL shaders that power cinematic, GPU-accelerated visual transitions between two textures, video frames, or images.

---

## 1. The GLSL Transition Specification

Every GL-transition conforms to a strict, deterministic GLSL function signature:

```glsl
// Uniforms provided by the runtime environment:
uniform sampler2D from;   // Source texture (current frame)
uniform sampler2D to;     // Destination texture (next frame)
uniform float progress;   // Transition progress: 0.0 (fully 'from') -> 1.0 (fully 'to')
uniform float ratio;      // Aspect ratio of the viewport (width / height)

// Built-in helper functions:
vec4 getFromColor(vec2 uv) {
  return texture2D(from, uv);
}

vec4 getToColor(vec2 uv) {
  return texture2D(to, uv);
}

// Required transition entrypoint:
vec4 transition(vec2 uv);
```

---

## 2. Classic Transition Examples

### A. Directional Wipe Transition

```glsl
// Directional wipe with smooth feathered edge
uniform vec2 direction; // e.g. vec2(1.0, -1.0)
uniform float smoothness; // e.g. 0.1

vec4 transition(vec2 uv) {
  vec2 v = normalize(direction);
  v /= (abs(v.x) + abs(v.y));
  float d = v.x * (uv.x - 0.5) + v.y * (uv.y - 0.5);
  float m = smoothstep(-smoothness, 0.0, v.x * (uv.x - 0.5) + v.y * (uv.y - 0.5) - (progress * (1.0 + smoothness) - 0.5));
  return mix(getFromColor(uv), getToColor(uv), m);
}
```

### B. Dynamic Ripple / Wave Distortion

```glsl
uniform float amplitude; // e.g. 30.0
uniform float speed;     // e.g. 20.0

vec4 transition(vec2 uv) {
  vec2 dir = uv - vec2(0.5);
  float dist = length(dir);
  vec2 offset = dir * (sin(progress * dist * amplitude - progress * speed) + 0.5) / 30.0;
  return mix(
    getFromColor(uv + offset),
    getToColor(uv),
    smoothstep(0.2, 1.0, progress)
  );
}
```

---

## 3. Integration with Remotion Video Engine

In Remotion projects, use `@remotion/gl-transitions` or `@remotion/transitions` for frame-accurate transitions:

```tsx
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { wipe } from '@remotion/transitions/wipe';

export const VideoTimelineWithTransitions: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={60}>
        <SceneA />
      </TransitionSeries.Sequence>

      {/* GPU transition */}
      <TransitionSeries.Transition
        presentation={wipe({ direction: 'from-left' })}
        timing={linearTiming({ durationInFrames={15} })}
      />

      <TransitionSeries.Sequence durationInFrames={60}>
        <SceneB />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

---

## 4. Standalone WebGL Canvas Runner (`gl-transition` npm)

```typescript
import createTransition from 'gl-transition';

export function runTransitionOnCanvas(
  gl: WebGLRenderingContext,
  glslCode: string,
  textureFrom: WebGLTexture,
  textureTo: WebGLTexture
) {
  const transition = createTransition(gl, glslCode);

  function render(progress: number) {
    gl.clear(gl.COLOR_BUFFER_BIT);
    transition.draw(progress, textureFrom, textureTo, gl.drawingBufferWidth, gl.drawingBufferHeight, {
      // Custom uniform values passed to the shader
      smoothness: 0.15,
      direction: [1.0, 0.0],
    });
  }

  return { render, dispose: () => transition.dispose() };
}
```

---

## 5. Critical Rules & Performance Checklist

- **Clamp UV Coordinates**: Always ensure UV coordinates stay within `[0.0, 1.0]` when using distortion or zoom shaders. Out-of-bounds UV sampling without clamping causes texture edge bleeding.
- **Normalize Vectors in Directional Shaders**: Always call `normalize(direction)` on custom uniform directional vectors to prevent aspect ratio distortion.
- **Account for `ratio`**: When computing circular distances (vignettes, ripples, circles), multiply `dir.x *= ratio` to keep circles perfectly round rather than squished ovals.
