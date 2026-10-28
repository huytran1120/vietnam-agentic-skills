---
name: psx-horror-style
category: design
description: >-
  PS1/PSX-era horror art direction combining low-poly affine textures, limited color depth, fog, and psychological horror staging for Blender assets.
risk: safe
source: https://github.com/arjun988/blender-skills
source_repo: arjun988/blender-skills
author: Arjun Shukla
license: MIT
tags: [blender, 3d, psx-horror, ps1-horror, puppet-combo, retro-horror, affine-texture, crunchy-lowpoly-horror, vhs-horror]
---


# PSX Horror Style

Crunchy low-poly horror. Affine textures. Fog. Limited palette. Tension over fidelity.

## When to Use

- PS1-era horror game looks
- Puppet Combo / retro survival horror vibes
- When `horror-style` needs explicit PSX constraints

## Core Tenets

1. **Low poly, high dread** — Few tris, strong shapes
2. **Texture crunch** — Low-res, nearest filtering feel
3. **Vertex / affine warping cues** — Subtle wobble optional
4. **Fog + darkness** — Hide draw distance sins
5. **Analog grit** — VHS/CRT via compositing sparingly

## Vs Related Styles

| Skill | Role |
|-------|------|
| `horror-style` | Broad psychological horror direction |
| `lowpoly-style` | General PS1/PS2 / Lethal Company |
| `psx-horror-style` | Horror + PSX crunch specifically |

## Modeling

- 100–800 tris for many props
- Characters chunky; faces minimal
- Interiors modular, repetitive, oppressive

## Materials / Textures

- 64–256px textures common
- Limited palette; indexed feel
- Flat shading or very low smooth
- Emissive screens as narrative props

## Lighting & Camera

- Single practical lights; deep shadows
- Low camera, narrow spaces
- Fog/mist mandatory for depth
- Optional handheld noise (`camera-cinematography`)

## Compositing Extras

- Slight blur / chromatic aberration
- Posterize / crush colors carefully
- Film grain / VHS overlay subtle

## Constraints

### MUST DO
- Keep poly and texture budgets intentionally low
- Prioritize fog, sound-design-friendly spaces
- Stage sparse narrative props

### MUST NOT DO
- Modern PBR microdetail as primary look
- Bright clean global illumination

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|----------|
| Psx Horror Budgets | `references/psx-horror-budgets.md` | When needed |
| Psx Horror Palette | `references/psx-horror-palette.md` | When needed |
