---
name: blender-mcp
category: design
tags: [blender, mcp, 3d, modeling, bpy, scene-generation, polyhaven, sketchfab, meshy, hunyuan3d]
risk: safe
description: >-
  Connect Blender 3D to any LLM via Model Context Protocol (MCP) for prompt-driven
  3D modeling, scene creation, material application, lighting, rigging, retopology,
  animation, and asset integration (Poly Haven, Sketchfab, Hyper3D Rodin, Meshy, Hunyuan3D).
---

# MCP for Blender (BlenderMCP)

Connect Blender to AI Coding Agents (Antigravity, Claude Code, Cursor, Windsurf, Codex) via the Model Context Protocol (`blender-mcp`) to directly inspect, create, modify, render, and animate 3D scenes in Blender using natural language and `bpy` scripts.

## Core Capabilities

1. **Two-Way Socket Communication**: Connects the MCP Server (`uvx blender-mcp`) to a custom Blender Add-on (`scripts/addon.py`) over a local TCP socket.
2. **Object & Scene Manipulation**: Create, delete, transform, and organize 3D meshes, cameras, lights, and collections.
3. **Material & Shader Control**: Procedural shader networks, PBR textures, and HDRIs.
4. **Asset Integrations**:
   - **Poly Haven**: Download HDRIs, textures, and 3D models via API.
   - **Sketchfab**: Search and import downloadable 3D models.
   - **AI 3D Generation**: Generate 3D meshes via Hyper3D (Rodin), Meshy, or Hunyuan3D.
5. **Execute Arbitrary Python (`execute_blender_code`)**: Run `bpy` code directly inside Blender context with viewport screenshot feedback (`get_viewport_screenshot`).

## Specialized Domain Guides

Before executing complex 3D workflows, read the relevant guide in `references/guides/`:
- **Scene Composition**: `references/guides/scene.md`
- **Blender Python (`bpy`) Best Practices**: `references/guides/bpy.md`
- **Materials & Shaders**: `references/guides/materials.md`
- **Level Design & Environment**: `references/guides/level-design.md`
- **Retopology & Mesh Cleanup**: `references/guides/retopology.md`
- **Rigging & Armatures**: `references/guides/rigging.md`
- **Animation & Keyframes**: `references/guides/animation.md`

## Quick Setup

1. **Install Blender Add-on**:
   - Open Blender (3.0+) -> `Edit > Preferences > Add-ons > Install...`
   - Select `scripts/addon.py` and enable **Interface: Blender MCP**.
   - In the 3D Viewport sidebar (`N`), open the **BlenderMCP** tab and click **Connect to MCP server**.
2. **Configure MCP Server**:
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "uvx",
         "args": ["blender-mcp"]
       }
     }
   }
   ```

## Recommended Workflow for Agents

1. Always call `get_scene_info` first to understand existing objects, materials, and world state.
2. Break complex 3D modeling into incremental steps (blocking -> detailing -> materials -> lighting).
3. After significant geometry or camera changes, capture the viewport (`get_viewport_screenshot`) to visually verify alignment, proportions, and lighting.
4. Prefer Poly Haven / Sketchfab assets for realistic props and HDRIs before procedural approximation.
