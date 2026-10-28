"""Drawing Session State Manager (Single Responsibility Principle).

Encapsulates active in-memory architectural specification, revision tracking,
and state transitions.
"""

from __future__ import annotations

import copy
import json
from typing import Any

from architect_cad_mcp.templates.registry import get_template


class DrawingSessionState:
    """Manages active drawing specification state and revision history."""

    def __init__(self, initial_template_id: str = "courtyard_residence") -> None:
        self._revision: int = 1
        self._active_spec: dict[str, Any] = get_template(initial_template_id)

    @property
    def revision(self) -> int:
        return self._revision

    @property
    def spec(self) -> dict[str, Any]:
        """Return deep copy of current active specification."""
        return copy.deepcopy(self._active_spec)

    def get_raw_spec(self) -> dict[str, Any]:
        """Return direct reference for read-only inspections."""
        return self._active_spec

    def update_spec(self, new_spec: dict[str, Any]) -> int:
        """Replace the active specification with a new one, bumping revision."""
        self._active_spec = copy.deepcopy(new_spec)
        self._revision += 1
        return self._revision

    def mutate_spec(self) -> tuple[dict[str, Any], int]:
        """Provide direct mutable reference for in-place modifications and bump revision."""
        self._revision += 1
        return self._active_spec, self._revision

    def reset_to_template(self, template_id: str) -> tuple[dict[str, Any], int]:
        """Reset state to a specific template."""
        self._active_spec = get_template(template_id)
        self._revision += 1
        return copy.deepcopy(self._active_spec), self._revision


# Global singleton drawing state for server session
SESSION_STATE = DrawingSessionState("courtyard_residence")


def ok_response(payload: dict[str, Any], revision: int | None = None) -> str:
    """Format standard successful JSON response with active revision."""
    rev = revision if revision is not None else SESSION_STATE.revision
    return json.dumps({"ok": True, "revision": rev, **payload}, indent=2)


def error_response(code: str, message: str, recommended_action: str | None = None) -> str:
    """Format standard error JSON response."""
    return json.dumps(
        {
            "ok": False,
            "isError": True,
            "error": {
                "code": code,
                "message": message,
                "recommended_action": recommended_action or "Check tool arguments and active spec.",
            },
        },
        indent=2,
    )
