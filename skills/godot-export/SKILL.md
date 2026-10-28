---
name: godot-export
category: design
description: >-
  Godot-specific Blender export favoring GLTF/GLB with correct scale, materials, animation clips, and collision shapes via MCP.
risk: safe
source: https://github.com/arjun988/blender-skills
source_repo: arjun988/blender-skills
author: Arjun Shukla
license: MIT
tags: [blender, 3d, godot, godot-export, godot-gltf, godot-glb, godot-materials, godot-animation]
---


# Godot Export

GLTF/GLB first. Clean nodes. Godot-friendly materials and animation.

## When to Use

- Shipping meshes/animations to Godot 4.x
- GLB single-file props and characters
- Simple collision companions

## Pre-Flight

1. `asset-optimization` PASS
2. Apply transforms; Y-up friendly hierarchy
3. Materials metallic-roughness compatible

## Format

| Case | Format |
|------|--------|
| Default | GLB |
| Editable sidecar textures | GLTF separate |

## Settings

```
Format: GLB
+Y Up
Apply Modifiers: ON (when final)
Animation: include when needed
```

## Hierarchy

- Root empty or object named for scene root
- Avoid deep useless empties
- Keep collision meshes clearly named `COL_` / `UCX_` style

## Materials

- Principled BSDF → GLTF PBR
- Pack images or keep relative paths consistent
- Emission only where intended

## Animation

- NLA or actions exported as clips
- Name actions `AN_[Clip]`
- Root motion documented if used

## Verify in Godot

- [ ] Scale
- [ ] Import materials
- [ ] Animation libraries
- [ ] Collision shapes

## Constraints

### MUST DO
- Prefer GLB unless project says otherwise
- Test import once
- Keep naming consistent with `naming-conventions.md`

### MUST NOT DO
- Rely on Blender-only shader nodes that do not export

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|----------|
| Godot Checklist | `references/godot-checklist.md` | When needed |
