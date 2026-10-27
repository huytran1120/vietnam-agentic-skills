---
name: matterjs
description: "2D rigid body physics simulation with Matter.js. Covers Engine, World, Bodies (rectangle, circle, polygon, fromVertices), Composite hierarchies, Constraints (springs, distance joints, elastic cords), MouseConstraint interactions, collision filtering (category, mask, group), collision events (collisionStart, collisionActive), restitution/friction/density physics tuning, sleep states, and headless simulation decoupled from custom Canvas/Pixi/Three.js renderers."
category: game-development
risk: safe
source: community
source_repo: "liabru/matter-js"
author: "liabru"
tags: ["matterjs", "physics-engine", "2d-physics", "rigid-body", "collision-detection", "canvas-physics", "simulation", "game-development"]
date_added: "2026-10-27"
---

# Matter.js — 2D Rigid Body Physics Engine

Matter.js is a battle-tested 2D rigid body physics engine for the web. It handles continuous collision detection, compound bodies, physical constraints, springs, friction, restitution, and sleep states.

---

## 1. Core Architecture & Decoupled Mental Model

```
+-----------------------------------------------------------+
|                       Matter.Engine                       |
|         (Physical Simulation, Collision Detection)        |
+-----------------------------------------------------------+
                              |
                     Matter.Composite (World)
        +---------------------+---------------------+
        |                     |                     |
  Matter.Bodies         Matter.Bodies      Matter.Constraint
  (Dynamic Box)         (Static Ground)    (Elastic Joint)
                              |
            +-----------------+-----------------+
            |                                   |
    Matter.Render                       Custom Renderer
 (Built-in Canvas Debugger)       (PixiJS / Three.js / DOM)
```

**Golden Rule**: For production web apps, games, and generative motion, decouple `Matter.Engine` from `Matter.Render`. Run physics headlessly via `Engine.update(engine, delta)` and render bodies using your own Canvas, SVG, or PixiJS loop.

---

## 2. Headless Physics Setup with Custom Render Loop

```typescript
import { Engine, Bodies, Composite, Runner, Body } from 'matter-js';

export function setupPhysicsWorld(canvasWidth: number, canvasHeight: number) {
  // 1. Create engine
  const engine = Engine.create({
    gravity: { x: 0, y: 1, scale: 0.001 },
  });

  // 2. Define static boundaries (Ground & Walls)
  const ground = Bodies.rectangle(canvasWidth / 2, canvasHeight + 30, canvasWidth, 60, {
    isStatic: true,
    restitution: 0.6, // Bounciness
    friction: 0.8,
  });

  const leftWall = Bodies.rectangle(-30, canvasHeight / 2, 60, canvasHeight, { isStatic: true });
  const rightWall = Bodies.rectangle(canvasWidth + 30, canvasHeight / 2, 60, canvasHeight, { isStatic: true });

  // 3. Spawn falling dynamic objects
  const boxes = Array.from({ length: 20 }, (_, i) => {
    return Bodies.rectangle(
      canvasWidth * 0.3 + Math.random() * (canvasWidth * 0.4),
      -50 - i * 40,
      40,
      40,
      {
        restitution: 0.5,
        friction: 0.1,
        angle: Math.random() * Math.PI,
      }
    );
  });

  // Add all bodies to the world
  Composite.add(engine.world, [ground, leftWall, rightWall, ...boxes]);

  // 4. Tick simulation forward
  function step(deltaTimeMs: number) {
    Engine.update(engine, deltaTimeMs);
  }

  return { engine, boxes, ground, step };
}
```

---

## 3. Collision Filtering (Categories & Masks)

Use bitwise masks to control which bodies can collide with each other:

```typescript
import { Bodies } from 'matter-js';

// Define collision categories as powers of 2
const CATEGORY_DEFAULT     = 0x0001; // 0001
const CATEGORY_PLAYER      = 0x0002; // 0010
const CATEGORY_COLLECTIBLE = 0x0004; // 0100
const CATEGORY_ENEMY       = 0x0008; // 1000

// Player collides with DEFAULT and COLLECTIBLE, but ignores ENEMY
const player = Bodies.circle(100, 100, 20, {
  collisionFilter: {
    category: CATEGORY_PLAYER,
    mask: CATEGORY_DEFAULT | CATEGORY_COLLECTIBLE,
  },
});

// Enemy collides with DEFAULT and other enemies, but ignores PLAYER
const enemy = Bodies.rectangle(300, 100, 40, 40, {
  collisionFilter: {
    category: CATEGORY_ENEMY,
    mask: CATEGORY_DEFAULT | CATEGORY_ENEMY,
  },
});
```

---

## 4. Elastic Constraints & Mouse Dragging

```typescript
import { Engine, Bodies, Constraint, Composite, Mouse, MouseConstraint } from 'matter-js';

export function attachMouseAndSpring(engine: Engine, canvasElement: HTMLCanvasElement) {
  // Pin an object with an elastic spring
  const bob = Bodies.circle(400, 300, 30, { restitution: 0.8 });
  const spring = Constraint.create({
    pointA: { x: 400, y: 100 }, // Fixed pin coordinate
    bodyB: bob,                 // Target body
    stiffness: 0.05,            // Elasticity (lower = more stretch)
    damping: 0.02,              // Energy dissipation
  });

  Composite.add(engine.world, [bob, spring]);

  // Add interactive mouse drag
  const mouse = Mouse.create(canvasElement);
  const mouseConstraint = MouseConstraint.create(engine, {
    mouse,
    constraint: {
      stiffness: 0.2,
      render: { visible: false },
    },
  });

  Composite.add(engine.world, mouseConstraint);
}
```

---

## 5. Collision Event Handling

```typescript
import { Events, Engine } from 'matter-js';

export function registerCollisionEvents(engine: Engine) {
  Events.on(engine, 'collisionStart', (event) => {
    const pairs = event.pairs;

    for (let i = 0; i < pairs.length; i++) {
      const { bodyA, bodyB } = pairs[i];

      // Check if player touched a collectible
      if (bodyA.label === 'player' && bodyB.label === 'coin') {
        collectCoin(bodyB);
      } else if (bodyB.label === 'player' && bodyA.label === 'coin') {
        collectCoin(bodyA);
      }
    }
  });
}
```

---

## 6. Critical Rules & Performance Checklist

- **Enable Sleep States**: Set `engine.enableSleeping = true`. Stationary objects will sleep and consume zero CPU cycles until struck by a moving body.
- **Never Modify `body.position` Directly During Step**: Direct mutation breaks velocity and impulse math. Use `Body.setVelocity(body, { x, y })` or `Body.applyForce(body, position, force)`.
- **Set Fixed Iterations**: Tune `engine.positionIterations` (default 6) and `engine.velocityIterations` (default 4). Reducing them slightly dramatically boosts performance on low-end mobile devices without noticeable stability loss.
