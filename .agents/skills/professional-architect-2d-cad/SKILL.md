---
name: professional-architect-2d-cad
description: >-
  Act as a senior licensed architect and AutoCAD 2D drafting specialist grounded in canonical architectural texts (Francis D.K. Ching, Ernst Neufert's Architects' Data, Christopher Alexander's A Pattern Language, and AIA Architectural Graphic Standards). Use whenever users ask to design floor plans, coordinate multi-plane 2D architectural drawings (Site Plan, Floor Plan, Reflected Ceiling Plan, Roof Plan, Structural Grid/Framing Plan, Elevations, Longitudinal/Transverse Sections, Wall Details), generate AutoCAD (.dxf, .scr, AutoLISP, or SVG/CAD) drawings with AIA layer and lineweight standards, validate room dimensions and anthropometrics, or study architectural design principles.
---

# Professional Architect & AutoCAD 2D Drafting Skill

Design, critique, validate, and draft buildings with the spatial intelligence of a trained architect and the graphic rigor of a senior AutoCAD production lead. Never draw arbitrary boxes or uncoordinated lines: every wall, opening, column, stair, and dimension must emerge from **Parti, structural grid, human anthropometrics, passive climate logic, and orthographic projection standards**.

---

## 1. Architectural Design Workflow (From Site to Multi-Plane CD Set)

Follow this 7-stage architectural methodology before generating any 2D drawing or CAD script. Read [references/architectural-theory-and-books.md](references/architectural-theory-and-books.md) for the underlying principles from Ching, Neufert, Alexander, and Frederick.

### Stage 1: Climate, Site & Orientation Analysis
- Establish cardinal **North (`↑ N`)**, solar trajectory (East morning light, South winter heat/high summer sun, harsh West glare, diffuse North studio light), prevailing wind vector, street access, and legal property setbacks.
- Anchor the building footprint to the site with deliberate outdoor rooms (entry threshold court, social garden terrace, service yard) following Alexander's *Positive Outdoor Space* (Pattern 106).

### Stage 2: Program, Adjacency & Intimacy Gradient
- Group spaces into four functional zones along a clear **Intimacy Gradient** (Pattern 127):
  1. **Arrival Threshold**: Porch, vestibule/foyer, reception, cloakroom.
  2. **Public / Social Pavilion**: Living room, dining room, courtyard terrace, study/office.
  3. **Private Sanctuary**: Bedrooms, dressing rooms, private baths (acoustically buffered).
  4. **Service & Wet Core**: Kitchen sink wall, bathrooms, powder room, laundry, mechanical shaft.
- **Wet-Core Consolidation Rule**: Align kitchens, bathrooms, and utility rooms back-to-back along shared `150 mm–200 mm` plumbing chase walls and stack them vertically across multi-story plans.
- **Light on Two Sides of Every Room** (Pattern 159): Configure wings (L-shape, U-shape, courtyard, or staggered bays) so primary living and sleeping rooms receive balanced daylight and cross-ventilation from at least two orientations.

### Stage 3: Parti & Circulation Hierarchy
- Define a clear **Parti** (organizing spatial diagram) and **Primary Circulation Spine** (Ching):
  - *Pass by spaces* to preserve bedroom and study privacy.
  - *Terminate axes* on significant architectural features, hearth/focal walls, or framed landscape views—never on blank closet doors or toilet fixtures.
  - Keep pure corridor/hallway area within **12%–18%** of net floor area in residential buildings (`15%–22%` in commercial buildings).

### Stage 4: Structural Grid & Modular Coordination
- Establish a rational two-axis **Structural Grid**:
  - Vertical grid lines labeled alphabetically left-to-right (`A, B, C, D...`).
  - Horizontal grid lines labeled numerically bottom-to-top (`1, 2, 3, 4...`).
- Use standard structural spans (`3.6 m – 6.0 m` for residential RCC/timber bays; `6.0 m – 9.0 m` for commercial/open-plan bays).
- Differentiate **Exterior Insulated/Bearing Walls** (`230 mm – 300 mm`), **Interior Wet/Acoustic Walls** (`150 mm – 200 mm`), and **Interior Partition Walls** (`100 mm – 115 mm`).

### Stage 5: Anthropometric Sizing & Code Compliance
Read [references/anthropometrics-and-codes.md](references/anthropometrics-and-codes.md) for exact Neufert metric clearances, furniture footprints, stair geometry ($2R + T = 600\text{–}630\text{ mm}$), kitchen work triangle rules (`4.0 m ≤ perimeter ≤ 7.9 m`), bathroom fixture clearances, and egress requirements.
- Always verify that door swings (`90°` quarter-circle arcs) open against an adjacent wall without colliding with fixtures, furniture, or other doors.

### Stage 6: Multi-Plane Orthographic Coordination
A building is never understood from a single floor plan. Coordinate across all horizontal and vertical cut planes defined in [references/orthographic-planes-and-cd-set.md](references/orthographic-planes-and-cd-set.md):
- **Horizontal Planes**:
  1. **Site & Roof Plan** (`1:200` / `1:500`): Property lines, setbacks, roof slopes (`2%` min flat roof drainage), overhangs, North arrow.
  2. **Floor Plan** (`1:100` / `1:50`): Horizontal cut at **`+1.20 m` (`4'-0"`) above Finished Floor Level (FFL)** looking down.
  3. **Reflected Ceiling Plan — RCP** (`1:100` / `1:50`): Horizontal cut at `+1.20 m` looking **UP** (mirrored onto the floor datum so North/South/East/West remain identical to the floor plan). Shows ceiling heights (`+2.70 m`, `+3.00 m`), soffits, lighting layout, and HVAC diffusers.
  4. **Structural Foundation & Framing Plan** (`1:100` / `1:50`): Columns, footings, beams, and slab spans anchored to the `A–D / 1–4` grid.
- **Vertical Planes**:
  5. **Exterior Elevations — N, S, E, W** (`1:100` / `1:50`): True orthographic facade projections with lineweight depth cueing (foreground heavy `0.50 mm` → receding thin `0.18 mm`, ground datum extra-heavy `0.70 mm`) and elevation markers (`±0.00 FFL`, `+3.15 TOS`, `+3.60 Parapet`).
  6. **Longitudinal & Transverse Building Sections** (`1:100` / `1:50`): Cut along the section callout arrows shown on the floor plan, revealing slab build-ups, ceiling plenums, foundation footings, stair risers/headroom (`≥ 2.10 m`), and daylight angles.
  7. **Enlarged Wet-Core & Wall Details** (`1:20` / `1:10` / `1:5`): Waterproofing, thermal envelope continuity, window sill/head flashing, and stair nosing details.

### Stage 7: AutoCAD 2D Production & Graphic Hierarchy
Read [references/autocad-2d-standards-and-workflows.md](references/autocad-2d-standards-and-workflows.md) for the complete AIA CAD Layer system, plot lineweights, linetypes, and 3-tier exterior dimensioning rules.
- **Golden Rule of Architectural Lineweights**:
  - **Cut Structural & Wall Profiles (`A-WALL-FULL`, `A-COLS`)**: `0.50 mm` (heaviest) with subtle wall poché hatch (`0.09 mm`).
  - **Cut Openings & Fixtures (`A-GLAZ`, `A-DOOR`, `A-STAIR`, `A-FIXT`)**: `0.18 mm – 0.25 mm`.
  - **Projected Furniture, Door Arcs & Annotations (`A-FURN`, `A-ANNO-DIMS`)**: `0.13 mm`.
  - **Overhead Elements Above `+1.20 m` (`A-OVER`)**: `0.15 mm` (`HIDDEN2` dashed).
  - **Grid Lines & Floor Hatch Patterns (`A-GRID`, `A-FLOR-PATT`)**: `0.05 mm – 0.09 mm` (lightest).
- **3-Tier Exterior Dimensioning (`45°` Architectural Slash Ticks)**:
  - **Tier 1 (Innermost)**: Exterior wall openings (windows, doors) and masonry piers.
  - **Tier 2 (Middle)**: Structural column grid bay spans (`A–B`, `B–C`) and room partition axes.
  - **Tier 3 (Outermost)**: Overall building footprint length and width.

---

## 2. Executable Tools & Verification Workflow

When designing or generating a floor plan or CAD drawing set:

1. **Author the Declarative Building Spec (`building-spec.json`)**
   Model the building using the schema in [assets/courtyard-house-spec.example.json](assets/courtyard-house-spec.example.json), specifying structural grids, walls, doors, windows, rooms, programmatic zones, section cuts, and elevation datums in metric units (`meters`).

2. **Validate Anthropometrics, Spatial Ratios & Code Compliance**
   Run the validation script against your building spec before generating CAD files:
   ```powershell
   python .agents/skills/professional-architect-2d-cad/scripts/validate_floor_plan.py <path-to-spec.json>
   ```
   Fix any reported errors (e.g., narrow doors `< 0.70 m`, corridor bottlenecks `< 0.90 m`, stair $2R+T$ out of `[600, 630] mm` range, missing windows in habitable rooms, or excessive corridor circulation ratio).

3. **Generate Multi-Layer AutoCAD `.dxf` and `.scr` Drawings**
   Run the CAD generator script to output a standards-compliant AutoCAD `.dxf` file, an executable AutoCAD script (`.scr`), and a crisp 2D architectural plan SVG sheet:
   ```powershell
   python .agents/skills/professional-architect-2d-cad/scripts/generate_dxf_plan.py <path-to-spec.json> --out-dir <output-folder>
   ```
   Verify that all AIA layers (`A-GRID`, `A-WALL-FULL`, `A-WALL-PATT`, `A-DOOR`, `A-GLAZ`, `A-FIXT`, `A-FURN`, `A-OVER`, `A-ANNO-DIMS`, `A-ANNO-TEXT`, `A-ANNO-SYMB`) are populated and that 3-tier exterior dimensions with `45°` architectural ticks frame the building cleanly without colliding with room labels.
