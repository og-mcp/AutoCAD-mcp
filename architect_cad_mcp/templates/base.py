"""Base model and protocol for architectural templates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ArchitecturalTemplate:
    """Immutable architectural template descriptor."""

    id: str
    name: str
    title: str
    category: str  # "house", "floor_building", "workplace"
    gross_area_m2: float
    description: str
    design_principles: list[str]
    spec: dict[str, Any]

    def to_summary(self) -> dict[str, Any]:
        """Return a lightweight metadata summary."""
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "category": self.category,
            "gross_area_m2": self.gross_area_m2,
            "description": self.description,
            "design_principles": self.design_principles,
        }
