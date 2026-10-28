# Orthographic Planes & Construction Document (CD) Drawing Set

A professional architect communicates a 3D building through a coordinated system of **2D orthographic planes**. Every horizontal and vertical cut plane must register geometrically (`X`, `Y`, `Z` coordinates) across all sheets.

---

## 1. Taxonomy of Architectural Drawing Planes

### Plane 01: Site & Context Plan (`Scale 1:500` or `1:200`)
- **Projection**: Top-down orthographic view above the highest roof canopy.
- **Mandatory Elements**:
  - Legal property boundary (`PHANTOM2` linetype, heavy `0.50 mm`) with bearings/lengths.
  - Setback lines (`DASHED` linetype, `0.18 mm`) defining buildable envelope.
  - Existing and proposed topography contours (`0.50 m` or `1.00 m` intervals).
  - Building roof footprint with ridge/valley lines, drainage slopes (`e.g., 2%`), and dashed ground footprint overhang.
  - Hardscape (driveways, entry paths, travertine plinths), landscape trees, water bodies, North arrow (`↑ N`), solar/wind rose, and street access arrows.

### Plane 02: Floor Plan (`Scale 1:100` or `1:50`)
- **Projection**: Horizontal section cut taken at **`+1.20 m` (`4'-0"`) above Finished Floor Level (FFL)**, looking vertically downward.
- **Three Depth Layers in Every Floor Plan**:
  1. **Cut Plane (`z = +1.20 m`)**: Full-height exterior walls, interior partitions, structural columns, window jambs/mullions, door frames, and stair risers below `+1.20 m`. Drawn with heaviest lineweight (`0.50 mm` for walls/columns, `0.25 mm` for glazing/frames) and wall poché (`0.09 mm`).
  2. **Below Cut Plane (`0.00 m ≤ z < +1.20 m`)**: Window sills, low parapet/balustrade walls, door leaves and `90°` swing arcs, thresholds, level steps, sanitary fixtures, kitchen counters, and furniture layouts. Drawn in continuous medium-to-thin lines (`0.13 mm – 0.20 mm`).
  3. **Above Cut Plane (`z > +1.20 m`)**: Roof cantilevers/overhangs, dropped structural beams, skylights, double-height void edges, archway soffits, and upper kitchen wall cabinets. Drawn in thin dashed lines (`HIDDEN2`, `0.15 mm`).

### Plane 03: Reflected Ceiling Plan — RCP (`Scale 1:100` or `1:50`)
- **Projection**: Horizontal cut at `+1.20 m` looking **UPWARD** via an imaginary mirror on the floor.
  - *Crucial Convention*: Do NOT flip the plan left-to-right. An RCP has the exact same wall footprint and North/South/East/West orientation as the Floor Plan so sheets overlay directly.
- **What Changes from the Floor Plan**:
  - Freeze furniture, plumbing fixtures, floor hatches, door leaves/swings, and window sills.
  - Show door headers/lintels across openings (where walls continue above the door head).
  - Add ceiling height tags inside diamond or oval callouts (`e.g., +2.70 m GYP. BD.`, `+3.10 m ACOUSTIC WOOD SLAT`).
  - Draft recessed downlights, linear LED coves, pendant fixtures, HVAC supply/return grilles, exhaust fans, smoke detectors, and switching circuitry loops (`SPLINE` dashed arcs from switches to luminaires).

### Plane 04: Structural Foundation & Framing Plan (`Scale 1:100` or `1:50`)
- **Projection**: Horizontal cut at foundation footing datum or structural slab soffit.
- **Mandatory Elements**:
  - Structural grid axes (`A, B, C...` vertical; `1, 2, 3...` horizontal) with grid bubbles and exact center-to-center bay dimensions.
  - Columns (`C1: 300×300 mm`), isolated pad footings (`F1: 1500×1500 mm`), continuous strip footings, grade beams (`GB1: 230×450 mm`), slab thicknesses (`S1: 150 mm RCC`), and two-way/one-way slab span symbols.

### Plane 05: Roof & Drainage Plan (`Scale 1:100` or `1:200`)
- **Projection**: Top-down orthographic view of the roof assembly.
- **Mandatory Elements**:
  - Parapet walls (`230 mm – 300 mm` with metal coping), roof drains (`RD`), overflow scuppers (`OS`), tapered insulation cricket lines, slope arrows (`MIN. 1:50 / 2% SLOPE TO DRAIN`), skylights, solar PV arrays, and mechanical curbs.

### Plane 06: Exterior Elevations — North, South, East, West (`Scale 1:100` or `1:50`)
- **Projection**: Vertical orthographic planes parallel to the four principal building facades, outside the building looking in.
- **Graphic Conventions**:
  - **Ground Line**: Extra-heavy continuous line (`0.70 mm`) extending at least `2.0 m` beyond the building footprint on both sides.
  - **Lineweight Depth Cueing**:
    - Closest projecting masses/canopies: `0.50 mm`
    - Primary facade plane: `0.35 mm`
    - Recessed courtyard walls: `0.25 mm`
    - Window mullions, siding joints, material hatches: `0.09 mm – 0.13 mm`
    - Underground foundations: `0.15 mm` (`DASHED`)
  - **Elevation Datum Markers**: Stacked along the left/right margins (`±0.00 FINISHED GROUND`, `+0.45 PLINTH FFL`, `+2.55 WINDOW HEAD / LINTEL`, `+3.45 TOP OF ROOF SLAB`, `+3.90 TOP OF PARAPET`).
  - **Window Operability Hinges**: Dashed diagonal `V` triangles pointing toward the hinged edge (casement/awning) or horizontal arrows (sliding panels).

### Plane 07: Building Sections — Longitudinal & Transverse (`Scale 1:100` or `1:50`)
- **Projection**: Vertical slicing planes cut right through the building along the section callout lines (`Section A-A`, `Section B-B`) marked on the Floor Plan.
- **Rules for Choosing Section Cut Locations**:
  - Always pass at least one section through **vertical circulation (stairs/elevators/ramps)**, **courtyards/double-height voids**, and **skylights/clerestories**.
  - Look in the exact direction indicated by the section arrows on the Floor Plan.
- **What Must Be Drawn**:
  - Cut earth/subgrade hatch below the ground line, compacted gravel bed (`150 mm`), damp-proof membrane (DPM), foundation footings, ground slab (`150 mm`), cut walls (`0.50 mm`), lintel beams, roof slab, insulation layer, and parapet upstand.
  - Uncut background interior elevations (doors, windows, casework, room heights) in thin lines (`0.13 mm – 0.18 mm`).

### Plane 08: Wall Sections & Construction Details (`Scale 1:20`, `1:10`, `1:5`)
- **Purpose**: Explains *how* materials join together so water, heat, air, and structural loads are controlled.
- **Four Critical Envelopes to Detail**:
  1. **Foundation-to-Plinth Junction**: Footing, stem wall, perimeter drainage pipe, waterproofing membrane, thermal break, and floor finish.
  2. **Window Sill & Head Detail**: Drip groove (`10 mm × 10 mm`) under exterior sill to prevent rainwater wicking, sloped sill (`≥ 15°`), thermal break aluminum/timber frame, sealant + backer rod, and lintel/roller-shade pocket at head.
  3. **Roof Edge / Parapet Detail**: Tapered insulation, waterproofing membrane turned up parapet (`min. 250 mm`), metal counter-flashing, and sloped parapet coping (`sloped inward toward roof drain`).
  4. **Wet-Room Floor Threshold**: `15 mm – 20 mm` recessed waterproof shower/bathroom slab drop with linear drain to prevent water migration into corridors.

---

## 2. Standard Sheet Numbering System (AIA / National CAD Standard)

Organize multi-sheet drawing packages using standard discipline and sheet type codes:

| Sheet Code | Sheet Title | Typical Scale |
| :--- | :--- | :--- |
| `G-001` | Cover Sheet, Drawing Index, Code Summary, Abbreviations & Symbols Legend | `N.T.S.` |
| `A-100` | Site Plan, Context Analysis, Solar/Wind Diagram & Roof Drainage Plan | `1:200` |
| `A-101` | Ground Floor Plan (Dimensioned, Room Tags, Area Schedule) | `1:50` / `1:100` |
| `A-102` | Furniture & Finish Floor Plan | `1:50` / `1:100` |
| `A-103` | Reflected Ceiling Plan (Lighting, Soffits, Diffusers) | `1:50` / `1:100` |
| `A-201` | Exterior Elevations (North, South, East, West) | `1:50` / `1:100` |
| `A-301` | Building Sections (Longitudinal Section A-A, Transverse Section B-B) | `1:50` / `1:100` |
| `A-401` | Enlarged Wet-Core Plans (Kitchen, Bathrooms) & Interior Elevations | `1:20` |
| `A-501` | Wall Sections, Stair Details & Window/Door Schedules | `1:20` / `1:10` / `1:5` |
| `S-101` | Structural Grid, Foundation & Slab Framing Plan | `1:50` / `1:100` |
| `M-101` / `E-101` / `P-101` | Mechanical HVAC, Electrical Power/Data & Plumbing Supply/Drainage Plans | `1:50` / `1:100` |
