---
name: rapier
description: "Cross-platform 2D and 3D physics engine written in Rust with fast WebAssembly bindings (@dimforge/rapier2d, @dimforge/rapier3d, @react-three/rapier). Covers World simulation, RigidBody types (dynamic, fixed, kinematicPositionBased, kinematicVelocityBased), Collider geometries (cuboid, ball, cylinder, capsule, trimesh, convex hull), Joints (revolute, prismatic, fixed, spherical), Raycasting, Contact manifolds, KinematicCharacterController, and integration with Three.js and React Three Fiber."
category: game-development
risk: safe
source: community
source_repo: "dimforge/rapier"
author: "dimforge"
tags: ["rapier", "rapier-physics", "webassembly", "3d-physics", "2d-physics", "collision-detection", "rust-physics", "threejs", "game-development"]
date_added: "2026-10-27"
---

# Rapier — High-Performance 2D & 3D WebAssembly Physics

Rapier is an ultra-fast, cross-platform physics engine written in Rust by the Dimforge team, compiled to WebAssembly for JavaScript/TypeScript environments. It powers deterministic, SIMD-accelerated 2D and 3D rigid body dynamics, joint constraints, raycasting, and character controllers.

---

## 1. Core Architecture: Bodies vs. Colliders

In Rapier, physical mass/motion is cleanly separated from shape geometry:

- **`RigidBody`**: Holds state, position, velocity, mass, damping, and motion type (`dynamic`, `fixed`, `kinematicPositionBased`, `kinematicVelocityBased`).
- **`Collider`**: Holds shape geometry (Cuboid, Ball, Cylinder, Capsule, TriMesh, ConvexHull), friction, restitution, and collision groups. Attached as children to a `RigidBody`.

---

## 2. Quickstart: 3D Physics with Rapier WebAssembly & Three.js

```typescript
import RAPIER from '@dimforge/rapier3d-compat';
import * as THREE from 'three';

export async function initRapierThreeScene() {
  // 1. Initialize WASM module
  await RAPIER.init();

  // 2. Create physical world with gravity
  const gravity = { x: 0.0, y: -9.81, z: 0.0 };
  const world = new RAPIER.World(gravity);

  // 3. Create static ground
  const groundBodyDesc = RAPIER.RigidBodyDesc.fixed().setTranslation(0, -0.5, 0);
  const groundBody = world.createRigidBody(groundBodyDesc);
  const groundColliderDesc = RAPIER.ColliderDesc.cuboid(10.0, 0.5, 10.0);
  world.createCollider(groundColliderDesc, groundBody);

  // 4. Create falling dynamic sphere
  const sphereBodyDesc = RAPIER.RigidBodyDesc.dynamic()
    .setTranslation(0.0, 8.0, 0.0)
    .setLinearDamping(0.1);
  const sphereBody = world.createRigidBody(sphereBodyDesc);
  const sphereColliderDesc = RAPIER.ColliderDesc.ball(1.0)
    .setRestitution(0.7) // Bouncy
    .setFriction(0.3);
  world.createCollider(sphereColliderDesc, sphereBody);

  // Three.js visual counterpart
  const sphereMesh = new THREE.Mesh(
    new THREE.SphereGeometry(1, 32, 32),
    new THREE.MeshStandardMaterial({ color: 0x38bdf8 })
  );

  // Simulation step loop
  function tick() {
    world.step();

    // Sync physical position & rotation to Three.js mesh
    const position = sphereBody.translation();
    const rotation = sphereBody.rotation();
    sphereMesh.position.set(position.x, position.y, position.z);
    sphereMesh.quaternion.set(rotation.x, rotation.y, rotation.z, rotation.w);
  }

  return { world, tick, sphereMesh };
}
```

---

## 3. Declarative 3D Physics with `@react-three/rapier`

For React Three Fiber projects, use the official declarative bindings:

```tsx
import React from 'react';
import { Canvas } from '@react-three/fiber';
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier';

export const PhysicsCanvas = () => {
  return (
    <Canvas camera={{ position: [0, 5, 10], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} />

      <Physics gravity={[0, -9.81, 0]} debug>
        {/* Dynamic Interactive Box */}
        <RigidBody colliders="cuboid" restitution={0.8}>
          <mesh position={[0, 5, 0]}>
            <boxGeometry args={[1.5, 1.5, 1.5]} />
            <meshStandardMaterial color="#6366f1" />
          </mesh>
        </RigidBody>

        {/* Fixed Ground */}
        <RigidBody type="fixed">
          <mesh position={[0, 0, 0]}>
            <boxGeometry args={[20, 0.5, 20]} />
            <meshStandardMaterial color="#1e293b" />
          </mesh>
        </RigidBody>
      </Physics>
    </Canvas>
  );
};
```

---

## 4. Precision Raycasting

```typescript
import RAPIER from '@dimforge/rapier3d-compat';

export function castLaserRay(world: RAPIER.World, origin: { x: number; y: number; z: number }, direction: { x: number; y: number; z: number }) {
  const ray = new RAPIER.Ray(origin, direction);
  const maxToi = 100.0; // Max ray distance
  const solid = true;   // Treat interiors as solid

  const hit = world.castRay(ray, maxToi, solid);
  if (hit != null) {
    const hitPoint = ray.pointAt(hit.toi);
    const collider = hit.collider;
    return { hitPoint, normal: hit.normal, collider };
  }
  return null;
}
```

---

## 5. Kinematic Character Controller

Rapier provides a built-in character controller for walking up stairs, sliding along walls, and snapping to ground:

```typescript
import RAPIER from '@dimforge/rapier3d-compat';

export function setupPlayerController(world: RAPIER.World, playerBody: RAPIER.RigidBody, playerCollider: RAPIER.Collider) {
  const offset = 0.05; // Skin offset
  const controller = world.createCharacterController(offset);

  controller.enableAutostep(0.5, 0.2, true); // Auto-step stairs up to 0.5m high
  controller.enableSnapToGround(0.5);        // Avoid floating when walking down slopes
  controller.setMaxSlopeClimbAngle((45 * Math.PI) / 180);

  function move(desiredMovement: { x: number; y: number; z: number }) {
    controller.computeColliderMovement(playerCollider, desiredMovement);
    const correctedMovement = controller.computedMovement();
    const currentPos = playerBody.translation();

    playerBody.setNextKinematicTranslation({
      x: currentPos.x + correctedMovement.x,
      y: currentPos.y + correctedMovement.y,
      z: currentPos.z + correctedMovement.z,
    });
  }

  return { controller, move };
}
```

---

## 6. Critical Rules & Memory Management

- **Always Call `RAPIER.init()` Before World Creation**: The WebAssembly binary must finish asynchronous compilation before calling any constructors.
- **Explicit Disposal**: Call `world.free()` and `controller.free()` when tearing down sessions to release Rust/WASM linear memory.
- **Use Convex Decompositions for Complex Meshes**: Never assign a raw TriMesh collider to a `dynamic` body (TriMeshes are only valid for `fixed` static obstacles). For dynamic complex geometries, compute a convex hull or compound convex decomposition (`VHACD`).
