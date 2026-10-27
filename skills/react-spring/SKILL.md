---
name: react-spring
description: "Master physics-based spring animations in React, Three.js (@react-spring/three), Web, and Canvas. Covers useSpring, useSprings, useTrail, useTransition, useChain, spring physics configuration (mass, tension, friction, velocity, clamp, bounce), fluid fluid gesture gestures with @use-gesture/react, imperative controllers, SVG morphing, and performant 60/120fps UI animations. Use when building physical, natural UI transitions, drag-and-drop interactions, staggering list reveals, page transitions, or 3D spring dynamics."
category: frontend
risk: safe
source: community
source_repo: "pmndrs/react-spring"
author: "pmndrs"
tags: ["react-spring", "spring-physics", "react-animation", "physics-based-animation", "web-animation", "pmndrs", "react"]
date_added: "2026-10-27"
---

# React Spring — Physics-Based Animation Engine

`react-spring` is a spring-physics based animation library that powers fluid, interruptible, and natural interactive motion in React, React Native, Three.js (`@react-spring/three`), and Canvas.

Unlike duration-and-curve animations (CSS transitions, easing curves), springs model real-world physical behavior: momentum, inertia, tension, and damping. When a user interrupts an ongoing animation, spring physics preserve velocity and seamlessly recalculate the trajectory without unnatural snapping.

---

## 1. Core Mental Model & Hook Selection

| Hook / API | Use Case | Mental Model |
| :--- | :--- | :--- |
| **`useSpring`** | Single animated value or state | An elastic rubber band connecting current value to target value. |
| **`useSprings`** | Multiple independent parallel springs | An array of independent physical springs (e.g., list items with independent drag states). |
| **`useTrail`** | Sequential wave/stagger animation | One spring leads; succeeding items follow with physics-driven trailing delays. |
| **`useTransition`** | Mounting, unmounting & list reordering | Orchestrates enter, update, and leave states for DOM elements (modals, accordions, lists). |
| **`useChain`** | Ordered orchestration between hooks | Defines deterministic execution queues and delays across multiple springs. |
| **`animated`** | High-performance wrapper | Bypasses React reconciliation by streaming updates directly to native DOM nodes. |

---

## 2. Spring Physics Parameters

```typescript
import { config } from '@react-spring/web';

// Pre-packaged presets:
// config.default  -> { mass: 1, tension: 170, friction: 26 }
// config.gentle   -> { mass: 1, tension: 120, friction: 14 }
// config.wobbly   -> { mass: 1, tension: 180, friction: 12 }
// config.stiff    -> { mass: 1, tension: 210, friction: 20 }
// config.slow     -> { mass: 1, tension: 280, friction: 60 }
// config.molasses -> { mass: 1, tension: 280, friction: 120 }

const customSpringConfig = {
  mass: 1,          // Inertia of the spring (higher = heavier, slower acceleration)
  tension: 180,     // Stiffness of the spring (higher = snappier, faster return)
  friction: 12,     // Dampening/resistance (lower = more oscillations/wobble)
  clamp: false,     // When true, stops immediately when crossing target (no overshoot)
  velocity: 0,      // Initial entry speed
  precision: 0.01,  // Precision threshold for resting state
  bounce: 0.25,     // Perceptual bounciness (0 = no bounce, 1 = hyper bouncy)
};
```

---

## 3. Production Patterns

### A. Fluid Interactive Toggle & Scale (`useSpring`)

```tsx
import React, { useState } from 'react';
import { useSpring, animated, config } from '@react-spring/web';

export const InteractiveButton: React.FC = () => {
  const [active, setActive] = useState(false);

  const styles = useSpring({
    transform: active ? 'scale(1.08)' : 'scale(1.0)',
    boxShadow: active
      ? '0 20px 35px -10px rgba(59, 130, 246, 0.45)'
      : '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    backgroundColor: active ? '#2563EB' : '#1E293B',
    config: config.wobbly,
  });

  return (
    <animated.button
      style={styles}
      onClick={() => setActive(!active)}
      className="px-6 py-3 rounded-xl text-white font-medium cursor-pointer"
    >
      {active ? 'Physics Active ⚡' : 'Click to Animate'}
    </animated.button>
  );
};
```

### B. Gestural Dragging with Velocity Handoff (`@use-gesture/react`)

```tsx
import React from 'react';
import { useSpring, animated, config } from '@react-spring/web';
import { useDrag } from '@use-gesture/react';

export const DraggableCard: React.FC = () => {
  const [{ x, y }, api] = useSpring(() => ({ x: 0, y: 0 }));

  const bind = useDrag(({ down, movement: [mx, my], velocity: [vx, vy], direction: [dx, dy] }) => {
    api.start({
      x: down ? mx : 0,
      y: down ? my : 0,
      immediate: down, // Follow pointer instantaneously during active drag
      config: {
        tension: 300,
        friction: 20,
        // Transfer pointer release velocity into spring rebound
        velocity: down ? 0 : Math.sqrt(vx * vx + vy * vy),
      },
    });
  });

  return (
    <animated.div
      {...bind()}
      style={{
        x,
        y,
        touchAction: 'none',
      }}
      className="w-48 h-48 bg-indigo-600 rounded-2xl shadow-xl cursor-grab active:cursor-grabbing flex items-center justify-center text-white"
    >
      Drag & Release Me
    </animated.div>
  );
};
```

### C. Mounting & Unmounting Transitions (`useTransition`)

```tsx
import React, { useState } from 'react';
import { useTransition, animated, config } from '@react-spring/web';

interface Item {
  id: string;
  text: string;
}

export const NotificationStack: React.FC = () => {
  const [items, setItems] = useState<Item[]>([
    { id: '1', text: 'Build succeeded' },
    { id: '2', text: 'Deploying to edge' },
  ]);

  const transitions = useTransition(items, {
    keys: (item) => item.id,
    from: { opacity: 0, height: 0, transform: 'perspective(600px) translate3d(0, -30px, -50px)' },
    enter: { opacity: 1, height: 50, transform: 'perspective(600px) translate3d(0, 0px, 0px)' },
    leave: { opacity: 0, height: 0, transform: 'perspective(600px) translate3d(0, 30px, -50px)' },
    config: config.gentle,
  });

  return (
    <div className="flex flex-col gap-2 w-80">
      {transitions((style, item) => (
        <animated.div
          style={style}
          className="bg-slate-900 border border-slate-800 rounded-lg p-3 text-sm text-slate-200 overflow-hidden shadow-lg flex justify-between items-center"
        >
          <span>{item.text}</span>
          <button
            onClick={() => setItems((prev) => prev.filter((i) => i.id !== item.id))}
            className="text-slate-400 hover:text-rose-400"
          >
            ✕
          </button>
        </animated.div>
      ))}
    </div>
  );
};
```

### D. Staggered Waterfall List (`useTrail`)

```tsx
import React, { useState } from 'react';
import { useTrail, animated, config } from '@react-spring/web';

export const TrailMenu: React.FC<{ items: string[]; open: boolean }> = ({ items, open }) => {
  const trail = useTrail(items.length, {
    config: config.stiff,
    opacity: open ? 1 : 0,
    x: open ? 0 : 20,
    height: open ? 40 : 0,
    from: { opacity: 0, x: 20, height: 0 },
  });

  return (
    <nav className="flex flex-col">
      {trail.map(({ height, ...style }, index) => (
        <animated.div
          key={items[index]}
          style={{
            ...style,
            height,
          }}
          className="overflow-hidden"
        >
          <div className="py-2 text-slate-300 font-medium hover:text-white cursor-pointer">
            {items[index]}
          </div>
        </animated.div>
      ))}
    </nav>
  );
};
```

---

## 4. Best Practices & Gotchas

1. **Avoid Animating Non-GPU Properties**: Always animate `transform` (`x`, `y`, `scale`, `rotate`) and `opacity` instead of `top`, `left`, `margin`, or `width` to avoid triggering browser layout recalculations.
2. **Never Unwrap `animated` Values in Render Loops**: Do not call `.get()` or convert animated spring values to primitive numbers inside the component render body. Pass them directly to `animated.div` style objects.
3. **Use Imperative APIs for High Frequency**: When handling drag, scroll, or cursor tracking, use `const [_, api] = useSpring(...)` and trigger `api.start({ ... })` inside callbacks rather than changing React state.
4. **Use `@react-spring/three` for 3D**: When animating Three.js objects inside `@react-three/fiber`, import from `@react-spring/three` to animate mesh properties (`position`, `rotation`, `scale`, `material-color`) without frame drops.
