# Diagram-to-Perspective Implementation Reference

Use these patterns when implementing an architectural diagram-to-perspective transition in React + TypeScript + Three.js + Anime.js.

## 1. Camera FOV Morph with Distance Compensation

When transitioning between a **parallel/axonometric architectural diagram** (`fov: 26°`) and a **human-scale perspective** (`fov: 48°`), keep the apparent framing size consistent by pairing the lower FOV with a proportionally longer camera-to-target distance:

```ts
// For a given target framing width W, camera distance scales inversely with tan(fov / 2):
// tan(42° / 2) / tan(26° / 2) ≈ 0.3839 / 0.2309 ≈ 1.66
// Stage 02 (Opening) -> Stage 03 (Axonometric Exploded Diagram):
timeline
  .add(
    pose,
    {
      camX: 16.5,
      camY: 28.5,
      camZ: 29.0,
      lookX: 0,
      lookY: 0.35,
      lookZ: 0.25,
      fov: 28,
      roofOpen: 1,
      shellOpen: 1,
      cutaway: 1,
      explode: 0.38,
      diagramOpacity: 0.85,
      duration: 900,
      ease: 'inOutCubic',
    },
    900,
  )
  .add(
    pose,
    {
      camX: 0.3,
      camY: 36.5,
      camZ: 33.5,
      lookX: 0,
      lookY: 0.15,
      lookZ: 0.35,
      fov: 26, // Crisp near-axonometric diagram projection
      explode: 1,
      diagramOpacity: 1,
      duration: 620,
      ease: 'inOutCubic',
    },
    1800,
  )
  // Smooth morph from 26° Axonometric Diagram into 48° Human-Scale Perspective inside Room 01
  .add(
    pose,
    {
      ...pBedroom,
      fov: 48,
      explode: ROOM_DETAIL_EXPLODE,
      detailDim: 1,
      diagramOpacity: 0,
      focus_bedroom: 1,
      duration: 660,
      ease: 'inOutCubic',
    },
    2520,
  )
```

## 2. 3D Architectural Drafting Overlay (`home.diagram`)

Build a dedicated `T.Group` for architectural diagram lines so their opacity and dynamic registration endpoints can be updated on every frame and cleanly disposed:

```ts
// 1. Dimension lines & 45-degree architectural slash ticks on the plinth datum (y = 0.03)
function addDimensionLine(
  parent: T.Group,
  mat: T.LineBasicMaterial,
  x1: number,
  z1: number,
  x2: number,
  z2: number,
  tickSize = 0.22,
) {
  const y = 0.03
  const pts = [
    new T.Vector3(x1, y, z1),
    new T.Vector3(x2, y, z2),
    // 45° architectural tick at start
    new T.Vector3(x1 - tickSize, y, z1 - tickSize),
    new T.Vector3(x1 + tickSize, y, z1 + tickSize),
    // 45° architectural tick at end
    new T.Vector3(x2 - tickSize, y, z2 - tickSize),
    new T.Vector3(x2 + tickSize, y, z2 + tickSize),
  ]
  const geom = new T.BufferGeometry().setFromPoints(pts)
  parent.add(new T.LineSegments(geom, mat))
}

// 2. 90-degree Door Swing Arcs on the floor plan datum
function addDoorSwingArc(
  parent: T.Group,
  mat: T.LineBasicMaterial,
  hingeX: number,
  hingeZ: number,
  radius: number,
  startAngle: number,
) {
  const y = 0.04
  const segments = 18
  const pts: T.Vector3[] = []
  // Door leaf line at open 90° position
  pts.push(
    new T.Vector3(hingeX, y, hingeZ),
    new T.Vector3(
      hingeX + Math.cos(startAngle + Math.PI * 0.5) * radius,
      y,
      hingeZ + Math.sin(startAngle + Math.PI * 0.5) * radius,
    ),
  )
  for (let i = 0; i < segments; i++) {
    const a0 = startAngle + (i / segments) * (Math.PI * 0.5)
    const a1 = startAngle + ((i + 1) / segments) * (Math.PI * 0.5)
    pts.push(
      new T.Vector3(hingeX + Math.cos(a0) * radius, y, hingeZ + Math.sin(a0) * radius),
      new T.Vector3(hingeX + Math.cos(a1) * radius, y, hingeZ + Math.sin(a1) * radius),
    )
  }
  parent.add(new T.LineSegments(new T.BufferGeometry().setFromPoints(pts), mat))
}
```

## 3. Dynamic Vertical Dashed Registration Lines

As the roof lifts (`+Y`) and the 6 room modules explode outward (`+X / +Z`), update the vertical dashed registration lines so they connect each displaced module back to its assembled plinth datum:

```ts
// Update dynamic registration line buffer in updateDiagram(roofOpen, explode, diagramOpacity):
// - 4 corners of the roof canopy -> plinth corners
// - 6 room centers (exploded position -> assembled plinth center)
registrationLine.computeLineDistances()
```
