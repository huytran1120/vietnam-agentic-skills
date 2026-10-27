---
name: gltf-transform
description: "CLI and TypeScript SDK for 3D glTF/GLB asset optimization, compression, and automated processing pipelines. Covers gltf-transform CLI commands (optimize, draco, meshopt, webp, ktx2, prune, dedup, flatten, weld, simplify), programmatic Document API, DRACO geometry compression, Meshopt decoding, Basis Universal / KTX2 GPU texture compression, LOD simplification, and glTF 2.0 validation."
category: graphics-processing
risk: safe
source: community
source_repo: "donmccurdy/glTF-Transform"
author: "donmccurdy"
tags: ["gltf-transform", "gltf", "glb", "3d-optimization", "draco-compression", "meshopt", "ktx2", "textures", "webgl", "graphics-processing"]
date_added: "2026-10-27"
---

# glTF Transform — 3D glTF & GLB Optimization Pipeline

`glTF-Transform` is the definitive CLI tool and TypeScript SDK for inspecting, optimizing, compressing, and transforming 3D assets in glTF and GLB formats. It shrinks multi-megabyte 3D models down to a fraction of their size for blazing-fast web delivery in Three.js, Babylon.js, and WebGL/WebGPU apps.

---

## 1. Essential CLI Commands

Install globally or execute via `npx` / Node script:

```bash
# 1. Quick all-in-one web optimization (prune, dedup, weld, meshopt, resize)
gltf-transform optimize input.glb output.glb --texture-compress webp

# 2. Draco geometry compression (high compression ratio for non-skinned models)
gltf-transform draco input.glb output.glb --method edgebreaker

# 3. Meshopt compression (faster GPU decoding, recommended for modern web apps)
gltf-transform meshopt input.glb output.glb --level medium

# 4. Convert all PNG/JPEG textures to ultra-efficient WebP
gltf-transform webp input.glb output.glb --quality 85

# 5. Compress textures to KTX2 / Basis Universal (GPU VRAM native texture decoding)
gltf-transform ktx2 input.glb output.glb --slots "{color,emissive}":uastc --slots "{normal,occlusion,metallicRoughness}":etc1s

# 6. Simplify polygon count (reduce draw calls & vertex count by 50%)
gltf-transform simplify input.glb output.glb --ratio 0.5 --error 0.001

# 7. Inspect metadata, mesh count, texture sizes & extensions
gltf-transform inspect model.glb
```

---

## 2. Programmatic TypeScript / Node.js Pipeline

```typescript
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import {
  prune,
  dedup,
  resample,
  weld,
  simplify,
  textureCompress,
} from '@gltf-transform/functions';
import sharp from 'sharp';
import { MeshoptSimplifier } from 'meshoptimizer';

export async function processModel(inputPath: string, outputPath: string) {
  const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
  const document = await io.read(inputPath);

  // Apply deterministic optimization transforms
  await document.transform(
    // 1. Remove unused textures, materials, and nodes
    prune(),
    // 2. Deduplicate identical materials and accessors
    dedup(),
    // 3. Weld duplicate vertices
    weld({ tolerance: 0.0001 }),
    // 4. Clean animation sampler timestamps
    resample(),
    // 5. Simplify complex geometry
    simplify({ simplifier: MeshoptSimplifier, ratio: 0.75, error: 0.002 }),
    // 6. Compress embedded textures to WebP using sharp
    textureCompress({
      encoder: sharp,
      targetFormat: 'webp',
      quality: 80,
      resize: [2048, 2048],
    })
  );

  await io.write(outputPath, document);
  console.log(`✓ Model successfully optimized and saved to ${outputPath}`);
}
```

---

## 3. Recommended Optimization Presets

| Target Scenario | Recommended Workflow | Key Flags / Extensions |
| :--- | :--- | :--- |
| **Landing Pages & E-Commerce** | `optimize` + WebP textures | `--texture-compress webp --compress meshopt` |
| **Heavy Architectural/CAD Visuals** | `simplify` + `weld` + Draco | `weld -> simplify (0.4) -> draco` |
| **Mobile WebGL & VR / WebGPU** | KTX2 Basis Universal textures | `--texture-compress ktx2` (Direct GPU upload, saves 80% VRAM) |
| **Animated Avatars & Characters** | `resample` + `meshopt` | Avoid Draco for complex bone weights; use Meshopt |

---

## 4. Critical Rules & Gotchas

- **Do Not Use Draco with High Bone/Weight Count**: Draco can introduce noticeable decompression latency on mobile devices for skinned character animations. Use `meshopt` instead for character models.
- **Maintain Power-of-Two (POT) Textures**: Ensure textures are scaled to POT dimensions (e.g., 1024×1024, 2048×2048) when converting to KTX2/Basis.
- **Always Run `prune()` and `dedup()` First**: Clean up dead nodes, orphan materials, and unreferenced buffer views before executing heavy mesh simplification or texture encoders.
