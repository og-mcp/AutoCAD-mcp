---
name: architectural-diagram-perspective
description: >-
  Design and build interactive architectural diagram-to-perspective animations that transition seamlessly from analytical architectural drawings (floor plan dimensions, Parti, programmatic zoning, circulation flow vectors, and exploded axonometric "layer cake" diagrams with vertical dashed registration lines) into human-scale 3D interior perspectives. Use whenever users ask to present architecture, floor plans, exploded axonometric diagrams, spatial zoning, or room-by-room tours that bridge how an architect reads a diagram with how a visitor experiences a living room in perspective.
---

# Architectural Diagram to Perspective Explainer

Create interactive 3D architectural experiences that bridge **analytical architectural diagrams** (orthographic/axonometric floor plans, exploded structural layers, dimension ticks, circulation spines, and programmatic zoning) with **immersive human-scale interior perspectives** (eye-level and intimate room views with realistic PBR materials, daylight, and living landscape).

## Core Architectural Diagram Principles

Synthesize three complementary architectural communication layers before stepping inside individual rooms:

1. **Floor Plan Conventions & Metric Dimensioning (SmartDraw Standard)**
   - **Dimension Lines & `45°` Architectural Ticks**: Frame the building plinth with true-to-scale metric callouts—both overall footprint spans (e.g., `15.60 m × 11.20 m · 174 m²`) and individual structural bay modules (`4.98 m × 5.28 m · 26.3 m²`) terminated with `45°` architectural slash ticks rather than generic arrowheads.
   - **Orientation & Graphic Scale**: Anchor every overview diagram with a cardinal North indicator (`↑ N`), a graphic scale bar (`SCALE 1:100`), and projection readout (`AXONOMETRIC 26° → PERSPECTIVE 48°`).
   - **Thresholds & Door Swing Arcs**: Draw `90°` quarter-circle door swing arcs and threshold ticks on the floor plan datum to show how entries open and how rooms connect without wall collisions.

2. **Exploded Axonometric "Layer Cake" & Registration Axes (Illustrarch Standard)**
   - **Vertical Stratification**: Separate the building along a shared vertical axis into distinct tectonic tiers:
     - `Tier 01`: Roof & Solar Canopy (lifts upward `+Y`)
     - `Tier 02`: Perimeter Structural Envelope & Glazing
     - `Tier 03`: Programmatic Room Modules (separate radially in `X/Z` from the central circulation spine)
     - `Tier 04`: Travertine Plinth, Courtyard Water & Living Landscape Datum
   - **Vertical Dashed Registration Lines**: Connect every lifted roof corner and exploded room module back to its exact assembled datum on the plinth using crisp 3D dashed vertical axes (`THREE.LineSegments` with `THREE.LineDashedMaterial`). This allows the viewer's eye to mentally snap the exploded diagram back together.

3. **Parti, Programmatic Zoning & Circulation Hierarchy (Archiroots Standard)**
   - **Parti & Spine**: Highlight the organizing central axis (e.g., East–West courtyard spine separating North and South wings).
   - **Programmatic Zoning**: Group spaces by acoustic, thermal, and social performance—such as **Private Sanctuary Wing** (North: Bedroom, Bathroom, Study) vs. **Social Garden Wing** (South: Living, Kitchen, Entrance Hall), with shared **Wet Core** plumbing walls clearly identified.
   - **Circulation Flow Vectors**: Trace the primary movement sequence across the plinth (`Entry Hall 06 → Kitchen 04 → Living 03 / Private Wing 01–02 & Study 05`) using a continuous directional vector path.

---

## Workflow: Diagram-to-Perspective Transition

Follow this 5-step sequence when building or upgrading an architectural 3D explainer:

### 1. Define the Architectural Registry
Extend each room/module in your catalog ([assets/diagram-storyboard.example.json](assets/diagram-storyboard.example.json)) with:
- `dimensions`: Metric bay width × depth (e.g., `'4.98 m × 5.28 m'`)
- `area`: Floor area in square meters (e.g., `'26.3 m²'`)
- `zone`: Programmatic zone label (`'PRIVATE SANCTUARY'`, `'WET CORE'`, `'SOCIAL PAVILION'`, `'ARRIVAL THRESHOLD'`)
- `assembledPosition` and `explodedOffset` in world meters.

### 2. Build the 3D Architectural Drafting Overlay Group
Read [references/diagram-to-perspective-implementation.md](references/diagram-to-perspective-implementation.md) for the exact Three.js geometry builders.
Create a dedicated `diagram` group inside the 3D scene containing:
- **Plinth Dimension Frame**: Outer footprint dimension lines with `45°` slash ticks and bay subdivision ticks along the North/West/East edges.
- **Vertical Dashed Registration Axes**: Dynamic dashed vertical lines connecting the 4 corners of the lifting roof canopy and each room module's anchor to the plinth datum (`y = 0.02`).
- **3D Circulation Spine & Door Swing Arcs**: Dashed circulation path with directional chevrons along the central corridor and `90°` threshold arcs at room entries.

### 3. Choreograph the Axonometric-to-Perspective Camera & FOV Morph
An architectural diagram reads best with minimal perspective foreshortening, whereas a room interior requires human-scale depth:
- **Stage 01 (`assembled`)**: Balanced exterior architectural three-quarter view (`fov: 38°–40°`).
- **Stage 02 (`opening`) & Stage 03 (`overview`)**: Morph the camera to a **low-FOV near-axonometric projection (`fov: 26°`)** while pulling the camera distance back proportionally (`d_axon ≈ d_persp * 1.55`) so parallel walls, structural bays, and floor-plan dimensions align like an architect's parallel axonometric drawing.
- **Stage 04+ (`detail` rooms `01..06`)**: As the camera glides down from the overview into Room 01 (`Bedroom`), smoothly interpolate `fov` from `26°` (axonometric diagram) to `48°` (human-scale interior perspective) while fading out the 3D drafting lines (`diagramOpacity → 0`) and bringing full-height room walls, tactile PBR materials, and garden views into focus.

### 4. Unobstructed Theater-Stage Cutaway & Continuous Interior Room Tour
- **Disable 360° Free Orbit Rotation During Scroll**: Free 360° camera rotation (`OrbitControls.enableRotate = true`) causes users to swing behind backdrop walls or get stuck on occluded angles during scroll transitions. Lock `controls.enabled = false` and drive the camera along a deterministic, unobstructed theater-stage trajectory with subtle human-scale breathing motion (`±0.05m`).
- **Continuous Wall Height Morphing (`walls.scale.y`)**: Instead of toggling full-height room walls on/off with a boolean at chapter boundaries (which causes walls to pop up in front of the camera while travelling between rooms), scale each room's backdrop walls smoothly using `settledFocus = Math.pow(focusWeight, 1.65)`. Walls lower to `0.18` cutaway height before the camera departs a room and rise smoothly to `1.0` full height only as the camera settles inside the next room.
- **Zero Foreground View Blockers**: Keep the front-center and front-right stage apron (`z > 0.3`) clear of tall glass partitions, vertical poles, or large plants so the camera lens never gets blocked. Place walk-in showers, tall bookshelves, and botanical plants in the rear/side corners to frame the room depth.
- **Two-Stage Interior Room Tour (`entryPose → tourPose`)**: Never freeze the camera while the user scrolls through a room chapter. Choreograph a continuous entry sweep (`entryPose`) followed by a gentle feature dolly-in (`tourPose`) paired with living interior motion (billowing sheer window drapes, diagonal warm sunbeam shafts, swaying brass pendants, rotating kinetic mobile, and rising spa bath steam/ripples).

### 5. Pair Projected 2D Callouts with an Architectural Drawing Legend
- During the `overview` stage (`phase === 'exploded'`), display projected SVG leader lines to each room chip alongside a compact **Architectural Drawing Legend / Scale Bar** (`PROJECTION: AXONOMETRIC 26°`, `FOOTPRINT: 15.60 m × 11.20 m · 174 m²`, `SCALE 1:100`, `↑ N`).
- During `detail` room stages (`phase === 'detail'`), hide the overview legend and bottom chrome so the visitor feels immersed inside the room, showing only a single floating room pin (`01 Bedroom · 26.3 m²`) that opens a crisp, short architectural card on click.

### 5. Verify Geometric & Visual Fidelity
Verify the transition with automated headless checks and screenshots:
1. At `overview` (`p ≈ 0.23`): `camera.fov <= 28`, `diagramOpacity > 0.8`, all 6 room leader lines project inside the viewport without overlapping, and vertical registration lines connect the lifted roof/modules to the plinth.
2. At `detail` (`p ≈ 0.33..0.83`): `camera.fov >= 46`, `diagramOpacity === 0`, the camera sits at human interior vantage with full-height room walls and living courtyard trees visible through the windows, and the detail drawer remains hidden until clicked.
3. At `reassemble` (`p ≈ 0.995`): `maxTransformDelta < 0.01` and all modules return to their exact assembled coordinates.
