# AutoCAD 2D Professional Drafting Standards & Workflows

Follow these industry-standard CAD conventions (AIA CAD Layer Guidelines / ISO 13567) when generating `.dxf` files, `.scr` scripts, AutoLISP routines, or 2D SVG architectural sheets.

---

## 1. Complete AIA Standard Layer, Color, Linetype & Lineweight Table

Always draft in **Model Space at 1:1 true scale** (`1 unit = 1 meter` or `1 unit = 1 millimeter`, explicitly declared in `$INSUNITS`). Assign every geometric entity to its semantic AIA layer:

| Layer Name | ACI Color | Hex (Dark UI / Plot) | Linetype | Plot Lineweight | Entities Assigned |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `A-GRID` | `8` (Gray) | `#64748B` | `CENTER2` | `0.09 mm` | Structural grid axes (`A–Z`, `1–99`) |
| `A-GRID-IDEN` | `7` (White/Black) | `#1E293B` | `Continuous` | `0.25 mm` | Grid bubbles (`Ø 8–10 mm` paper) & axis labels |
| `A-COLS` | `7` (White/Black) | `#0F172A` | `Continuous` | `0.50 mm` | Structural columns & load-bearing piers |
| `A-WALL-FULL` | `7` (White/Black) | `#0F172A` | `Continuous` | `0.50 mm` | Cut exterior & interior full-height walls |
| `A-WALL-PRHT` | `2` (Yellow) | `#334155` | `Continuous` | `0.25 mm` | Low walls, balustrades, planters (`< 1.20 m`) |
| `A-WALL-PATT` | `253` (Light Gray)| `#94A3B8` | `Continuous` | `0.09 mm` | Wall poché fill / diagonal masonry hatch |
| `A-DOOR` | `3` (Green) | `#1E293B` | `Continuous` | `0.20 mm` | Door jambs, door panels (`90°` open), thresholds |
| `A-DOOR-SWNG` | `8` (Gray) | `#64748B` | `Continuous` | `0.13 mm` | Quarter-circle (`90°`) door swing clearance arcs |
| `A-GLAZ` | `4` (Cyan) | `#0284C7` | `Continuous` | `0.25 mm` | Window mullions, glass panes (`2 lines`), curtain walls |
| `A-GLAZ-SILL` | `8` (Gray) | `#475569` | `Continuous` | `0.13 mm` | Exterior/interior window sill lines below cut |
| `A-STAIR` | `3` (Green) | `#334155` | `Continuous` | `0.20 mm` | Stair treads, handrails, diagonal cut break line, UP arrow |
| `A-FIXT` | `5` (Blue) | `#334155` | `Continuous` | `0.18 mm` | WCs, sinks, bathtubs, showers, kitchen casework/appliances |
| `A-FURN` | `252` (Gray) | `#64748B` | `Continuous` | `0.13 mm` | Beds, sofas, dining tables, chairs, study desks |
| `A-FLOR-LEVL` | `6` (Magenta) | `#475569` | `Continuous` | `0.15 mm` | Plinth edge, terrace steps, recessed wet-zone thresholds |
| `A-FLOR-PATT` | `254` (Very Light)| `#CBD5E1` | `Continuous` | `0.05 mm` | Wet-room tile grid, timber deck planks, courtyard water |
| `A-OVER` | `1` (Red) | `#64748B` | `HIDDEN2` | `0.15 mm` | Roof canopy overhang, beams, skylights above `+1.20 m` |
| `A-SITE-LAND` | `92` (Moss Green) | `#15803D` | `Continuous` | `0.15 mm` | Courtyard trees, planters, stepping stones, water basins |
| `A-ANNO-DIMS` | `6` (Magenta) | `#334155` | `Continuous` | `0.13 mm` | 3-tier exterior dimensions with `45°` architectural ticks |
| `A-ANNO-TEXT` | `7` (White/Black) | `#0F172A` | `Continuous` | `0.20 mm` | Room names, room numbers (`01`), area tags (`26.3 m²`) |
| `A-ANNO-SYMB` | `7` (White/Black) | `#0F172A` | `Continuous` | `0.25 mm` | Section cut markers (`A-A`), North arrow, level markers |
| `A-TTLB` | `7` (White/Black) | `#0F172A` | `Continuous` | `0.35 mm` | Sheet border, title block, graphic scale bar |

---

## 2. Step-by-Step AutoCAD 2D Floor Plan Construction Sequence

Follow this exact order to eliminate cumulative drafting errors:

### Step 1: Units, Limits & Grid Axes (`A-GRID`)
1. Set drawing units to Metric (`meters` with `0.00` precision or `millimeters` with `0` precision).
2. Draw vertical grid lines (`A, B, C, D`) and horizontal grid lines (`1, 2, 3`) extending `1.80 m` beyond the outer building perimeter on all four sides.
3. Place numbered/lettered circular grid bubbles (`r = 0.35 m` at `1:100` scale) at the ends of each grid line.

### Step 2: Exterior & Interior Wall Double-Lines (`A-WALL-FULL`)
1. Offset exterior walls (`0.24 m – 0.30 m` total thickness) and interior walls (`0.12 m – 0.20 m` thickness) from the structural grid lines.
2. Clean all wall intersections (`T-junctions`, `L-corners`, `X-crossings`) using `TRIM` and `FILLET (Radius = 0)` so the wall cavity forms a continuous, clean poché polygon with no internal cross-lines across wall junctions.

### Step 3: Punching Door & Window Openings (`A-DOOR`, `A-GLAZ`)
1. Locate door openings at **`0.10 m – 0.15 m` nib offset** from the adjacent perpendicular wall corner (allows space for door casing and light switches).
2. Trim the wall lines cleanly across each door and window opening, capping the cut wall jamb ends with `0.50 mm` perpendicular segments.
3. Draw each **Door Assembly**:
   - Jamb stops (`0.04 m × wall thickness`).
   - Door leaf rectangle (`0.045 m` thick × `door width`) rotated `90°` open against the adjacent wall.
   - Quarter-circle (`90°`) swing arc on `A-DOOR-SWNG` from the closed latch point to the open door tip.
4. Draw each **Window Assembly**:
   - Outer and inner sill lines on `A-GLAZ-SILL` flush with the exterior and interior wall faces.
   - Frame jambs (`0.05 m` wide) and double center glass lines (`0.04 m` apart) on `A-GLAZ`.

### Step 4: Stairs, Plinths, Casework & Sanitary Fixtures (`A-STAIR`, `A-FIXT`, `A-FURN`)
1. **Stairs**: Draw parallel riser lines spaced at exact tread depth (`T = 0.28 m – 0.30 m`), handrails (`0.05 m` offset), a central travel line with an arrow labeled `UP 18R`, and a `45°` diagonal break line with break zig-zag at the `7th–8th` riser (`+1.20 m` cut height); draw risers above the break line as dashed.
2. **Wet Core Fixtures**: Draft true-to-scale WCs (`0.40 m × 0.68 m`), vanity basins (`0.60 m` deep), walk-in glass showers (`min. 0.90 m × 1.20 m` with diagonal drain slopes), bathtubs (`1.70 m × 0.80 m`), and kitchen counters (`0.60 m` deep with double-bowl sink and 4-burner cooktop).
3. **Furniture Layout**: Populate every room with scaled furniture (`King bed 1.80 m × 2.00 m + nightstands`, `Dining table + chairs`, `Sofa group`, `Study desk`) to prove functional clearances and circulation lanes.

### Step 5: Roof Overhang & Wall Poché (`A-OVER`, `A-WALL-PATT`)
1. Offset the roof canopy perimeter (`0.60 m – 1.20 m` eaves overhang) outside the exterior walls on layer `A-OVER` (`HIDDEN2` dashed).
2. Apply solid light-gray poché or `ANSI31` diagonal masonry hatch inside all cut wall segments on `A-WALL-PATT`.

### Step 6: Three-Tier Exterior Dimensioning & Room Schedules (`A-ANNO-DIMS`, `A-ANNO-TEXT`)
1. Place **3 concentric exterior dimension strings** along the North, South, East, and West sides:
   - **String 1 (`0.90 m` offset from wall)**: Window widths, door widths, and masonry pier segments (must sum to String 3).
   - **String 2 (`1.50 m` offset from wall)**: Structural grid bay distances (`A–B`, `B–C`, `C–D`).
   - **String 3 (`2.10 m` offset from wall)**: Overall exterior building footprint length and width.
2. Terminate every dimension segment with **`45°` architectural slash ticks** (`0.18 m` tick length) and `0.15 m` extension line overshoots.
3. Place a centered **Room Tag Block** inside every room containing:
   - Room Number (`01`, `02`...) in a pill/box
   - Room Name (`MASTER BEDROOM`)
   - Net Floor Area (`26.3 m²`) and Finished Floor Level (`FFL +0.45`)
   - Programmatic Zone (`PRIVATE SANCTUARY`)
4. Add **Section Cut Markers** (`Section A-A` longitudinal, `Section B-B` transverse), **Cardinal North Arrow (`↑ N`)**, **Graphic Scale Bar (`0  1  2  5 m`)**, and **Title Block**.
