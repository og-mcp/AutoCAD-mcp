# Architect-CAD-MCP (`architect-cad-mcp`)

**Autonomous 2D Architectural CAD MCP Server Grounded in Canonical Design Theory (Francis D.K. Ching, Ernst Neufert, Christopher Alexander, Matthew Frederick).**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker Ready](https://img.shields.io/badge/Docker-Multi--stage%20%7C%20Non--root-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![Headless: ezdxf](https://img.shields.io/badge/Headless-ezdxf%20%7C%20Any%20Platform-brightgreen.svg)]()
[![AIA CAD Standards](https://img.shields.io/badge/AIA-25%20Standard%20Layers-informational.svg)]()
[![Neufert DRC](https://img.shields.io/badge/DRC-Neufert%20%2B%20IBC%20Compliant-success.svg)]()
[![MCP Standards](https://img.shields.io/badge/MCP-Tools%20%2B%20Resources%20%2B%20Prompts-purple.svg)]()

---

## 1. Clean Code & SOLID Architecture

`architect-cad-mcp` is engineered adhering strictly to **SOLID Design Principles** and clean architecture:

- **Single Responsibility Principle (SRP)**:
  - Every module has exactly one reason to change.
  - `core/layers.py` defines CAD standards and line weights.
  - `domain/drc/validator.py` handles Neufert and building code validations.
  - `domain/audit/dxf_audit.py` computes SHA-256 geometry digests and validates modelspace bounds.
  - `domain/rendering/png_renderer.py` produces byte-deterministic PNGs via Matplotlib Agg backend.
  - `domain/engines/walls.py` performs cut-wall poché and opening interval subtraction.
  - `domain/engines/multi_plane.py` coordinates 2D orthographic projections.
  - `state.py` manages active session specifications and revision history.
  - `health.py` provides independent diagnostics for container liveness and readiness probes.
- **Open/Closed Principle (OCP)**:
  - **Adding new MCP Tools**: Place a new tool module in `architect_cad_mcp/tools/` and register it in `architect_cad_mcp/tools/__init__.py`. No modification of server internals required.
  - **Adding new Templates**: Create a file in `architect_cad_mcp/templates/` (`houses/`, `buildings/`, or `workplaces/`) and add it to `registry.py` (or invoke `register_template`).
  - **Adding new Resources or Prompts**: Drop a module in `architect_cad_mcp/resources/` or `architect_cad_mcp/prompts/`.
- **Liskov Substitution Principle (LSP)**:
  - All templates conform to the uniform `ArchitecturalTemplate` protocol.
  - Audit and rendering engines operate on abstract document representations.
- **Interface Segregation Principle (ISP)**:
  - Modular separation between geometry creation, geometric auditing, visual rendering, and CAD script generation.
- **Dependency Inversion Principle (DIP)**:
  - High-level MCP tools and application factories depend on domain services and abstractions, not monolithic implementation files.

---

## 2. Directory & Package Structure

```
auto-cad-mcp/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                    # Unified CI/CD (Test matrix -> Docker verify -> Docker Hub publish)
├── architect_cad_mcp/                   # Clean root Python package
│   ├── __init__.py                      # Package root and public API
│   ├── __main__.py                      # CLI runner (python -m architect_cad_mcp)
│   ├── app.py                           # FastMCP Application Factory & Assembler
│   ├── health.py                        # Built-in health & diagnostic probe service
│   ├── server.py                        # MCP server instance & CLI argument parsing
│   ├── state.py                         # DrawingSessionState manager (SRP)
│   ├── core/                            # Domain Standards & Data Models
│   │   ├── __init__.py
│   │   ├── layers.py                    # 25 AIA CAD layers, lineweights, color palettes
│   │   ├── constants.py                 # Neufert dimensions, Blondel limits, codes
│   │   └── models.py                    # Strongly typed dataclasses
│   ├── domain/                          # Business Logic & Drafting Engines
│   │   ├── __init__.py
│   │   ├── audit/
│   │   │   ├── __init__.py
│   │   │   └── dxf_audit.py             # Structured geometry audit and SHA-256 digest
│   │   ├── drc/
│   │   │   ├── __init__.py
│   │   │   └── validator.py             # Neufert anthropometrics, Blondel, daylighting
│   │   ├── engines/
│   │   │   ├── __init__.py
│   │   │   ├── annotations.py           # 3-tier dimensions, slash ticks, grid bubbles, datums
│   │   │   ├── multi_plane.py           # 6 Coordinated Orthographic Planes generator
│   │   │   └── walls.py                 # Cut walls with solid poché & opening subtraction
│   │   └── rendering/
│   │       ├── __init__.py
│   │       └── png_renderer.py          # Byte-deterministic Matplotlib Agg PNG renderer
│   ├── templates/                       # Modular Architectural Templates (Open/Closed)
│   │   ├── __init__.py
│   │   ├── base.py                      # ArchitecturalTemplate protocol
│   │   ├── registry.py                  # Template registry and discovery service
│   │   ├── houses/                      # Residential typologies
│   │   │   ├── __init__.py
│   │   │   ├── courtyard_residence.py
│   │   │   ├── modern_family_villa.py
│   │   │   └── compact_townhouse.py
│   │   ├── buildings/                   # Multi-unit typologies
│   │   │   ├── __init__.py
│   │   │   └── apartment_floor.py
│   │   └── workplaces/                  # Workplace & studio typologies
│   │       ├── __init__.py
│   │       ├── open_office.py
│   │       └── atelier_studio.py
│   ├── tools/                           # Modular MCP Tools (Extensible!)
│   │   ├── __init__.py                  # register_all_tools(mcp)
│   │   ├── system.py                    # Server status and standards query tool
│   │   ├── template.py                  # Template inspection & instantiation tool
│   │   ├── drawing.py                   # Drawing lifecycle, audit, & export tool
│   │   ├── arch_element.py              # Wall, room, door, window, stair, furniture tool
│   │   ├── orthographic_plane.py        # Coordinated 2D plane projection tool
│   │   ├── annotation.py                # Drafting annotations, markers, title block tool
│   │   ├── arch_audit.py                # Neufert DRC & compliance tool
│   │   └── autocad_live.py              # AutoCAD live & script replay tool
│   ├── resources/                       # MCP Resources (@mcp.resource support!)
│   │   ├── __init__.py                  # register_all_resources(mcp)
│   │   ├── standards.py                 # cad://standards/layers, cad://standards/furniture-catalog, cad://standards/drc-rules
│   │   ├── templates.py                 # cad://templates/catalog, cad://templates/{category}/{template_id}
│   │   └── drawings.py                  # cad://drawing/active/spec, cad://drawing/active/drc, cad://drawing/active/planes
│   └── prompts/                         # MCP Prompts (@mcp.prompt support!)
│       ├── __init__.py                  # register_all_prompts(mcp)
│       ├── house.py                     # Prompt: design_house
│       ├── apartment.py                 # Prompt: design_apartment_floor
│       ├── workplace.py                 # Prompt: design_workplace
│       ├── audit.py                     # Prompt: audit_floor_plan
│       └── cd_package.py                # Prompt: generate_coordinated_cd_set
├── cad_output/                          # Generated DXF, SCR, SVG, and PNG packages (git-ignored)
├── demo-output/                         # Headless demo artifacts (git-ignored)
├── examples/
│   └── headless_demo.py                 # Pure ezdxf headless verification script
├── lisp-code/
│   └── mcp_arch_dispatch.lsp           # Optional AutoLISP dispatcher for AutoCAD
├── scripts/
│   ├── build_house_plan.py              # House plan generator
│   ├── build_floor_building.py          # Apartment floor building generator
│   ├── build_workplace_plan.py          # Workplace generator
│   └── build_all_templates.py           # Batch all-template generator
├── tests/
│   ├── test_architect_mcp.py            # MCP server & architectural tests
│   ├── test_headless_ezdxf.py           # Headless ezdxf & deterministic PNG tests
│   └── test_mcp_features.py             # MCP Resources, Prompts, & Extensibility tests
├── .dockerignore                        # Hardened Docker build context exclusion rules
├── .gitignore                           # Git ignore rules for clean repository
├── .mcp.json                            # MCP server declaration
├── Dockerfile                           # Multi-stage secure Docker container (appuser:10001)
├── docker-compose.yml                   # Docker Compose configuration (SSE service)
├── Makefile                             # install / test / build / publish targets
├── pyproject.toml                       # Python package configuration (Hatchling)
└── README.md                            # Complete technical manual
```

---

## 3. How to Easily Add New MCP Tools

Thanks to the modular registry pattern, adding a new tool takes less than 10 lines of code:

### Step 1: Create a new tool file in `architect_cad_mcp/tools/solar.py`
```python
from mcp.server.fastmcp import FastMCP
from architect_cad_mcp.state import SESSION_STATE, ok_response

def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def solar_analysis(azimuth_deg: float = 180.0, latitude_deg: float = 37.77) -> str:
        """Analyze solar orientation for South/North facades."""
        spec = SESSION_STATE.spec
        # Compute passive solar performance
        return ok_response({
            "solar_orientation": "Optimal South solar exposure",
            "azimuth": azimuth_deg,
            "latitude": latitude_deg,
        })
```

### Step 2: Register it in `architect_cad_mcp/tools/__init__.py`
```python
from architect_cad_mcp.tools import solar

TOOL_MODULES = [
    # ... existing tools ...
    solar.register,
]
```
The new tool is immediately available in MCP clients (Claude Desktop, Antigravity, Cursor) with full schema reflection!

---

## 4. MCP Resources (`cad://...`)

`architect-cad-mcp` exposes read-only architectural data as URI-addressable MCP Resources:

| URI | Description | MIME Type |
| :--- | :--- | :--- |
| `cad://standards/layers` | Complete 25-layer AIA layer definitions with lineweights and colors. | `application/json` |
| `cad://standards/furniture-catalog` | Standard Neufert furniture and sanitary fixture dimensions. | `application/json` |
| `cad://standards/drc-rules` | Neufert room areas, Blondel stair laws, and daylight code limits. | `application/json` |
| `cad://templates/catalog` | Catalog of ready-to-use templates across all 3 typologies. | `application/json` |
| `cad://templates/{category}/{template_id}` | Full architectural specification JSON for a specific template. | `application/json` |
| `cad://drawing/active/spec` | Real-time active in-memory architectural building specification. | `application/json` |
| `cad://drawing/active/drc` | Real-time Neufert anthropometrics and code compliance audit report. | `application/json` |
| `cad://drawing/active/planes` | Coordinated 2D orthographic planes and sheet metadata. | `application/json` |

---

## 5. MCP Prompts (`@mcp.prompt`)

AI clients can present interactive, pre-configured architectural prompt workflows directly to users:

| Prompt Name | Parameters | Purpose |
| :--- | :--- | :--- |
| **`design_house`** | `site_width_m`, `site_depth_m`, `bedroom_count`, `include_courtyard`, `style` | Guided prompt for residential design following Ching grids and Alexander courtyard patterns. |
| **`design_apartment_floor`** | `footprint_width_m`, `footprint_depth_m`, `unit_count`, `floor_to_floor_h` | Multi-family residential floor layout with elevator/stair cores and ADA corridors. |
| **`design_workplace`** | `headcount`, `footprint_width_m`, `footprint_depth_m`, `workplace_type` | Commercial agile workplace planning with boardroom, phone booths, and social cafe. |
| **`audit_floor_plan`** | `strict_neufert`, `check_daylight`, `check_blondel_stairs` | Code compliance audit checklist validating room sizes, glazing ratios, and stair ergonomics. |
| **`generate_coordinated_cd_set`**| `output_directory`, `dpi`, `render_png_previews` | Full 6-plane Construction Document generation (A-101 to S-101) with 3-tier dimensions. |

---

## 6. Ready-to-Use Architectural Templates

The server includes 6 complete, fully articulated architectural templates ready for immediate generation:

### A. Residential Houses
1. **`courtyard_residence`** (174.7 m²):
   - U-shaped introspective design inspired by Ching & Alexander (Pattern 115).
   - Central landscaped private courtyard with master suite, living pavilion, kitchen/dining, and covered breezeway.
2. **`modern_family_villa`** (226.8 m²):
   - 3-bedroom, 2-bath contemporary family residence.
   - Dual-zone public/private layout, open-plan kitchen with central island, walk-in closets, and garage storage.
3. **`compact_urban_townhouse`** (100.8 m²):
   - Narrow-lot urban residence ($7.2\text{m} \times 14.0\text{m}$).
   - Internal lightwell providing bilateral daylighting (Alexander Pattern 159), compact core, and efficient circulation ($<12\%$).

### B. Multi-Unit Floor Building
4. **`multi_unit_apartment_floor`** (345.6 m²):
   - Typical floor plate containing **5 residential units**:
     - Unit A & B: 2-Bedroom Family Units ($60.0\text{ m}^2$).
     - Unit C & D: 1-Bedroom Executive Units ($42.0\text{ m}^2$).
     - Unit E: Compact Studio ($32.0\text{ m}^2$).
   - Central pressurized core: 2 high-speed passenger elevators, pressurized fire escape stairwell ($1.2\text{m}$ clear run), MEP riser chase, and $1.6\text{m}$ wide central corridor.

### C. Workplaces & Studios
5. **`open_workplace_office`** (384.0 m²):
   - Modern open-plan agile office for 32 occupants.
   - Executive boardroom ($10\text{–}12$ seats), 2 private focus/phone booths, wellness/break room, and consolidated utility core.
6. **`architectural_atelier_studio`** (172.8 m²):
   - Creative design studio with natural north light.
   - Drafting zone, central model-making workshop bench, print/plotter room, and pin-up critique presentation gallery.

---

## 7. The 6 Coordinated Orthographic Planes

Every design in `architect-cad-mcp` is coordinated across 6 orthographic drawing sheets:

| Sheet | Orthographic Plane | Projection Details | Key Elements & AIA Layers |
| :--- | :--- | :--- | :--- |
| **A-101** | **Ground Floor Plan** | Horizontal cut at `+1.20m` looking down | Cut walls with poché (`A-WALL-FULL`, `A-WALL-PATT`), door swings (`A-DOOR`), windows (`A-GLAZ`), fixtures (`A-FLOR-FIXT`), 3-tier dimensions (`A-DIMS`), grid bubbles (`A-GRID-IDEN`). |
| **A-102** | **Reflected Ceiling Plan (RCP)** | Horizontal mirror cut at ceiling looking up | Ceiling grid outline (`A-CLNG`), recessed lighting fixtures (`E-LITE`), HVAC diffusers/returns (`M-HVAC-DIFF`), smoke detectors. |
| **A-103** | **Roof & Drainage Plan** | Overhead plan view looking down | Parapet walls (`A-ROOF`), roof slope directions with slope arrows (`2%`), drainage valleys, scuppers/downspouts (`A-ROOF-PATT`). |
| **A-201** | **Exterior Elevations** | South & North orthographic vertical projections | Plinth line (`±0.00`), window/door fenestrations, sill line (`+0.90`), lintel line (`+2.40`), roof parapet (`+3.60`), vertical datum level markers with dimension chains. |
| **A-301** | **Building Sections** | Longitudinal (`A-A`) & Transverse (`B-B`) cuts | Cut foundation slab (`-0.45m`), ground floor slab (`±0.00`), cut walls with concrete hatch, ceiling plane, roof slab, and clear floor-to-ceiling dimension chains. |
| **S-101** | **Structural Foundation & Framing** | Sub-grade and floor framing plan | Isolated column footings (`S-FOOT`), structural reinforced concrete columns (`S-COLS`), grade beams (`S-BEAM`), structural grid lines and column callouts. |

---

## 8. Docker Deployment & Hardened Container Architecture

`architect-cad-mcp` includes a production-grade, multi-stage, hardened Docker container designed for maximum security, reproducibility, and zero-display headless execution.

### Security & Hardening Features:
- **Multi-Stage Build**: Compiles dependencies in a temporary build stage; the runtime image contains zero compilers, development headers, or package managers.
- **Least-Privilege Non-Root Execution**: Runs as dedicated `appuser` (`UID 10001:10001`) with no login shell (`/usr/sbin/nologin`).
- **No External Display Server**: Fully headless `ezdxf` geometry engine and `MPLBACKEND=Agg` (zero X11/Wayland dependencies).
- **Built-in Diagnostic Health Check**: Container includes `HEALTHCHECK` with a 30s interval testing server tools, templates, ezdxf engine, and Neufert DRC validator.

### A. Build the Image
```bash
docker build -t architect-cad-mcp:latest .
```

### B. Verify Container Health
Run the built-in diagnostic probe directly inside the container:
```bash
docker run --rm architect-cad-mcp:latest --health
```
Output:
```json
{
  "status": "healthy",
  "server": "architect-cad-mcp",
  "version": "1.0.0",
  "checks": {
    "mcp_server": {
      "status": "PASS",
      "tools_registered": 8,
      "resources_registered": 7,
      "prompts_registered": 5,
      "resource_templates_registered": 1
    },
    "templates": {
      "status": "PASS",
      "templates_loaded": 6,
      "sample_verified": "TRAVERTINE COURTYARD RESIDENCE"
    },
    "drc_validator": {
      "status": "PASS",
      "checks_passed": 22,
      "errors": 0
    },
    "ezdxf_engine": {
      "status": "PASS",
      "dxf_version": "AC1027",
      "insunits": { "code": 6, "name": "meters" }
    },
    "matplotlib_agg": {
      "status": "PASS",
      "backend": "Agg",
      "headless_compatible": true
    }
  }
}
```

### C. Run via Docker in Stdio Mode (MCP Clients)
Mount your local `./cad_output` folder to receive generated DXF and PNG files:
```bash
docker run -i --rm -v "${PWD}/cad_output:/app/cad_output" architect-cad-mcp:latest
```

### D. Run via Docker Compose in Network / SSE Mode
Start the container as a detached network background service:
```bash
docker compose up -d
```
Inspect logs and health status:
```bash
docker compose ps
docker compose logs -f
```

---

## 9. MCP Client Configurations

### Claude Desktop Configuration
Add the following to your `claude_desktop_config.json`:

#### Option 1: Native Python (Stdio)
```json
{
  "mcpServers": {
    "architect-cad-mcp": {
      "command": "architect-cad-mcp",
      "args": []
    }
  }
}
```

#### Option 2: Docker Container (Stdio with Persistent Output Directory)
```json
{
  "mcpServers": {
    "architect-cad-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "${PWD}/cad_output:/app/cad_output",
        "architect-cad-mcp:latest"
      ]
    }
  }
}
```

#### Option 3: Network SSE Service
```json
{
  "mcpServers": {
    "architect-cad-mcp": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

---

### Cursor Configuration
Add to `.cursor/mcp.json` or Global Cursor Settings:
```json
{
  "mcpServers": {
    "architect-cad-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "${PWD}/cad_output:/app/cad_output",
        "architect-cad-mcp:latest"
      ]
    }
  }
}
```

---

### Antigravity Configuration
Add to `.mcp.json` in your project root:
```json
{
  "mcpServers": {
    "architect-cad-mcp": {
      "command": "architect-cad-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

---

## 10. Local Development & Verification

### Local Installation
```powershell
# Clone the repository
git clone https://github.com/your-username/architect-cad-mcp.git
cd auto-cad-mcp

# Install in editable mode
pip install -e ".[dev]"
```

### Run Full Test Suite (12 Tests)
```powershell
pytest -v
# ============================= 12 passed in 18.61s =============================
```
- Neufert DRC compliance across all 6 templates: **PASS**
- FastMCP tool invocations end-to-end: **PASS**
- Headless ezdxf status and geometry digest round-trip: **PASS**
- Byte-identical deterministic PNG generation: **PASS**
- All 6 coordinated orthographic planes rendered to PNG: **PASS**
- MCP Resources registered and readable: **PASS**
- MCP Prompts registered and callable: **PASS**
- Custom tool extensibility verified: **PASS**

### Run Diagnostic Health Check
```powershell
architect-cad-health
```

### Run Builder Scripts
```powershell
# Run headless ezdxf pipeline demo (DRC + DXF + PNG + SHA-256 Digest)
python examples/headless_demo.py

# Build all 3 House Templates (Courtyard, Villa, Townhouse) across 6 planes
python scripts/build_house_plan.py

# Build Multi-Unit Residential Floor Building across 6 planes
python scripts/build_floor_building.py

# Build Workplace Office & Atelier Studio across 6 planes
python scripts/build_workplace_plan.py

# Batch generate all 6 templates (36 DXF + 36 SCR + 36 SVG sheets)
python scripts/build_all_templates.py
```

---

## 11. Publishing to GitHub & Container Registries

### Pushing to GitHub
```bash
# Initialize and commit
git add .
git commit -m "feat: complete architectural 2D CAD MCP server with multi-stage Docker"

# Link remote repository and push
git remote add origin https://github.com/<your-username>/architect-cad-mcp.git
git branch -M main
git push -u origin main
```

### Publishing to Docker Hub (Makefile)
The [`Makefile`](Makefile) reads the version from `pyproject.toml` and builds a multi-arch (`linux/amd64`, `linux/arm64`) image tagged `:<version>` and `:latest`:
```bash
make version                          # -> 1.0.0
make build                            # local single-arch image
docker login
make publish DOCKER_USERNAME=<your-dockerhub-user>
```

### Automated CI/CD & Publish via GitHub Actions
The unified pipeline [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) runs on pushes to `main` and Pull Requests:
1. **Test Stage**: Runs tests, health check, and headless demo across Python 3.10, 3.11, and 3.12.
2. **Docker Verify Stage**: Builds the image, verifies non-root UID 10001, and runs container health check.
3. **Publish Stage** (main branch only): Compares `version` in `pyproject.toml` between `HEAD^` and `HEAD`. If bumped (or if manually triggered with `force: true`), logs into Docker Hub and publishes multi-arch images (`linux/amd64`, `linux/arm64`) tagged with `:<version>` and `:latest`.

Required repository secrets (*Settings → Secrets and variables → Actions*):

| Secret | Value |
| :--- | :--- |
| `DOCKER_USERNAME` | Docker Hub username / org |
| `DOCKER_PASSWORD` | Docker Hub access token (Account Settings → Personal access tokens) |

To release a new image: bump `version` in `pyproject.toml`, commit, and push to `main`.

### Publishing to GitHub Container Registry (GHCR)
```bash
# Log in to GHCR
echo $CR_PAT | docker login ghcr.io -u <your-github-username> --password-stdin

# Tag and push
docker tag architect-cad-mcp:latest ghcr.io/<your-github-username>/architect-cad-mcp:latest
docker push ghcr.io/<your-github-username>/architect-cad-mcp:latest
```

---

## 12. Theoretical Grounding & Canonical Literature

`architect-cad-mcp` is founded on canonical architectural design literature:
1. **Francis D.K. Ching** – *Architecture: Form, Space, and Order* (Structural bays, spatial hierarchy, axis, grid proportion).
2. **Ernst Neufert & Peter Neufert** – *Architects' Data* (Standard anthropometric clearances, living room dimensions, bathroom layout ergonomics).
3. **Christopher Alexander et al.** – *A Pattern Language* (Courtyards Which Live #115, Light on Two Sides of Every Room #159, Cascade of Roofs #116).
4. **Matthew Frederick** – *101 Things I Learned in Architecture School* (Poché solid/void ratio, room dimensions as human containers).
5. **AIA (American Institute of Architects)** – *CAD Layer Guidelines* (A-WALL, A-DOOR, A-GLAZ, A-FLOR-FIXT, S-COLS, A-DIMS).
6. **IBC (International Building Code)** – Means of Egress, occupant loads, minimum clear door widths ($813\text{ mm}$), corridor clearances ($1200\text{–}1800\text{ mm}$), Blondel stair law ($600 \le 2R + T \le 640\text{ mm}$).

---

## 13. License

Distributed under the **MIT License**. See `LICENSE` for details.
