---
name: paperjs
description: "Vector graphics scripting, Bézier curve math, and SVG manipulation with Paper.js on HTML5 Canvas. Covers Scene Graph (Project, Layer, Item, Path, CompoundPath), Bézier handles and curve geometry, boolean path operations (unite, intersect, subtract, exclude), path smoothing and simplify, vector arithmetic, interactive tool event loops, SVG import/export, and raster pixel sampling."
category: graphics-processing
risk: safe
source: community
source_repo: "paperjs/paper.js"
author: "paperjs"
tags: ["paperjs", "vector-graphics", "bezier-curves", "canvas", "svg", "path-math", "boolean-operations", "graphics-processing"]
date_added: "2026-10-27"
---

# Paper.js — Vector Graphics Scripting & Bézier Mathematics

Paper.js is the Swiss Army Knife of vector graphics scripting for HTML5 Canvas. It offers an expressive scene graph model, precision Bézier curve mathematics, automated path smoothing, boolean path operations (unite, subtract, intersect), and bidirectional SVG integration.

---

## 1. Setup & Scoped PaperScope Architecture

In modern JavaScript/TypeScript, never run Paper.js in global polluting mode (`paper.install(window)`). Always instantiate a dedicated `PaperScope`:

```typescript
import paper from 'paper';

export function setupVectorCanvas(canvasElement: HTMLCanvasElement) {
  const scope = new paper.PaperScope();
  scope.setup(canvasElement);

  // All shapes and layers created here belong exclusively to this scope
  const circle = new scope.Path.Circle({
    center: [150, 150],
    radius: 80,
    fillColor: '#38bdf8',
    strokeColor: '#0284c7',
    strokeWidth: 4,
  });

  scope.view.onFrame = (event: { count: number; delta: number; time: number }) => {
    circle.position.x += Math.sin(event.time * 2) * 1.5;
  };

  return scope;
}
```

---

## 2. Advanced Bézier Manipulation & Smooth Deformation

```typescript
import paper from 'paper';

export function createLiquidBlob(scope: paper.PaperScope, center: [number, number], radius: number) {
  const path = new scope.Path();
  path.fillColor = new scope.Color(0.2, 0.4, 0.9, 0.8);
  path.closed = true;

  const segments = 8;
  for (let i = 0; i < segments; i++) {
    const angle = (i / segments) * Math.PI * 2;
    const x = center[0] + Math.cos(angle) * radius;
    const y = center[1] + Math.sin(angle) * radius;
    path.add(new scope.Point(x, y));
  }

  // Automatically compute optimal Bézier control handles
  path.smooth({ type: 'continuous' });

  // Animate individual control points
  const originalPoints = path.segments.map((s) => s.point.clone());

  function updateBlob(time: number) {
    for (let i = 0; i < path.segments.length; i++) {
      const seg = path.segments[i];
      const orig = originalPoints[i];
      const wave = Math.sin(time * 3 + i) * 15;
      seg.point.x = orig.x + Math.cos(i) * wave;
      seg.point.y = orig.y + Math.sin(i) * wave;
    }
    path.smooth({ type: 'continuous' });
  }

  return { path, updateBlob };
}
```

---

## 3. Constructive Solid Geometry: Boolean Path Operations

Paper.js executes complex 2D boolean clipping directly in the browser:

```typescript
import paper from 'paper';

export function createCrescentMoon(scope: paper.PaperScope) {
  const baseCircle = new scope.Path.Circle({
    center: [200, 200],
    radius: 100,
  });

  const cutterCircle = new scope.Path.Circle({
    center: [250, 180],
    radius: 90,
  });

  // Subtract cutter from base shape
  const crescent = baseCircle.subtract(cutterCircle) as paper.Path;
  crescent.fillColor = new scope.Color('#facc15');

  // Clean up source geometry
  baseCircle.remove();
  cutterCircle.remove();

  return crescent;
}

// Available Boolean Operations:
// - path1.unite(path2)      -> Union of both shapes
// - path1.intersect(path2)  -> Overlapping area only
// - path1.subtract(path2)   -> Cut path2 out of path1
// - path1.exclude(path2)    -> Symmetric difference (XOR)
```

---

## 4. Bidirectional SVG Import & Export

```typescript
import paper from 'paper';

// Import SVG from markup or URL
export function loadAndTransformSVG(scope: paper.PaperScope, svgString: string) {
  const importedItem = scope.project.importSVG(svgString, {
    expandShapes: true, // Converts primitives (<rect>, <circle>) to editable <path>
    onLoad: (item: paper.Item) => {
      item.scale(1.5);
      item.strokeColor = new scope.Color('#ffffff');
      item.strokeWidth = 2;
    },
  });

  return importedItem;
}

// Export clean SVG DOM string
export function exportCurrentArtboardSVG(scope: paper.PaperScope): string {
  const svgNode = scope.project.exportSVG({
    asString: true,
    precision: 3,
    matchShapes: true,
  }) as string;

  return svgNode;
}
```

---

## 5. Critical Rules & Performance Checklist

- **Remove Intermediate Boolean Shapes**: Boolean operations (`unite`, `subtract`, `intersect`) return brand new Path items. Always invoke `.remove()` on source paths if they are no longer needed on the stage.
- **Limit Path Segment Count**: Avoid paths with thousands of raw points. Run `path.simplify(tolerance)` to reduce vertices while preserving curvature fidelity.
- **Dispose Scopes on Unmount**: When destroying an interactive canvas, call `scope.project.clear()` and `scope.remove()` to prevent retained Canvas contexts in memory.
