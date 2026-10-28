"""Domain Data Models for Architectural Specifications.

Strongly typed, validated data structures representing architectural elements,
orthographic projections, and drawing packages.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GridAxis:
    id: str
    axis: str  # "X" or "Y"
    coord: float
    label: str


@dataclass
class Column:
    id: str
    x: float
    y: float
    width: float = 0.30
    depth: float = 0.30
    material: str = "reinforced_concrete"


@dataclass
class Wall:
    id: str
    x1: float
    y1: float
    x2: float
    y2: float
    thickness: float = 0.20
    is_exterior: bool = False


@dataclass
class Door:
    id: str
    wall: str
    x: float
    y: float
    width: float = 0.90
    hand: str = "RH"  # "RH" (Right Hand) or "LH" (Left Hand)
    swing: str = "in"  # "in" or "out"
    type: str = "interior"  # "entry", "interior", "bathroom"


@dataclass
class Window:
    id: str
    wall: str
    room: str
    x1: float
    y1: float
    x2: float
    y2: float
    sill: float = 0.90
    head: float = 2.40


@dataclass
class Room:
    id: str
    name: str
    type: str  # "living", "primary_bedroom", "kitchen", "bathroom", etc.
    x: float
    y: float
    width: float
    depth: float
    habitable: bool = True
    wet_room: bool = False
    shared_wet_wall: str | None = None
    target_lux: int = 300


@dataclass
class Stair:
    id: str
    x: float
    y: float
    width: float = 1.00
    run: float = 2.80
    riser_mm: float = 175.0
    tread_mm: float = 280.0
    direction: str = "UP"


@dataclass
class FurnitureItem:
    id: str
    catalog_key: str
    room: str
    x: float
    y: float
    rotation: float = 0.0


@dataclass
class SectionCut:
    id: str  # e.g. "A-A", "B-B"
    x1: float
    y1: float
    x2: float
    y2: float
    view_dir: str = "N"


@dataclass
class ProjectMetadata:
    title: str = "UNTITLED PROJECT"
    client: str = "PRIVATE CLIENT"
    project_number: str = "ARCH-2026-001"
    drawn_by: str = "AI ARCHITECT"
    checked_by: str = "SENIOR ARCHITECT"
    date: str = "2026-10-28"
    scale: str = "1:100"
    units: str = "meters"
    building_type: str = "house"  # "house", "floor_building", "workplace"
    gross_area_m2: float = 0.0
    floor_to_ceiling_h: float = 3.00
    plinth_level: float = 0.45
    parapet_h: float = 3.60
    foundation_depth: float = 1.20
    grid_bays_x: list[float] = field(default_factory=list)
    grid_bays_y: list[float] = field(default_factory=list)


@dataclass
class ArchitecturalSpec:
    project: ProjectMetadata = field(default_factory=ProjectMetadata)
    grids: list[GridAxis] = field(default_factory=list)
    columns: list[Column] = field(default_factory=list)
    walls: list[Wall] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)
    doors: list[Door] = field(default_factory=list)
    windows: list[Window] = field(default_factory=list)
    stairs: list[Stair] = field(default_factory=list)
    furniture: list[FurnitureItem] = field(default_factory=list)
    sections: list[SectionCut] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert specification to JSON-serializable dictionary."""
        return asdict(self)
