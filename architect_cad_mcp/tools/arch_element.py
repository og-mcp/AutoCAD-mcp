"""Parametric architectural element creation tool (walls, rooms, doors, windows, stairs, furniture)."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from architect_cad_mcp.core.constants import FURNITURE_AND_FIXTURE_CATALOG
from architect_cad_mcp.state import SESSION_STATE, error_response, ok_response


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def arch_element(
        operation: str,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str:
        """Create or modify semantic 2D architectural elements on the active floor plan.

        Operations:
        - add_wall: Add a double-line wall (`id`, `x1`, `y1`, `x2`, `y2`, `thickness`, `type`).
        - add_room: Add a programmatic room (`id`, `name`, `type`, `zone`, `habitable`, `wetRoom`, `x`, `y`, `width`, `depth`, `ceilingHeight`).
        - punch_door: Add a door with 90-degree swing arc (`id`, `room`, `x`, `y`, `width`, `orientation`, `type`).
        - punch_window: Add a double-line glazed window with sill (`id`, `room`, `wall`, `x1`, `y1`, `x2`, `y2`, `sill`, `head`).
        - add_stair: Add an ergonomic staircase checked against Blondel's Law (`id`, `name`, `riserMm`, `treadMm`, `riserCount`, `widthM`, `x`, `y`).
        - place_furniture: Place a Neufert furniture/fixture block inside a room (`room_id`, `item`, `x`, `y`).
        """
        payload: dict[str, Any] = {}
        if data and isinstance(data, dict):
            payload.update(data)
        payload.update(kwargs)

        spec, rev = SESSION_STATE.mutate_spec()

        if operation == "add_wall":
            new_wall = {
                "id": payload.get("id", f"W-{len(spec.get('walls', [])) + 1:02d}"),
                "x1": float(payload["x1"]),
                "y1": float(payload["y1"]),
                "x2": float(payload["x2"]),
                "y2": float(payload["y2"]),
                "thickness": float(payload.get("thickness", 0.15)),
                "type": payload.get("type", "interior"),
            }
            spec.setdefault("walls", []).append(new_wall)
            return ok_response({"wall_count": len(spec["walls"]), "added": new_wall}, revision=rev)

        if operation == "add_room":
            room = {
                "id": str(payload.get("id", f"{len(spec.get('rooms', [])) + 1:02d}")),
                "name": str(payload["name"]),
                "type": str(payload.get("type", "living")),
                "zone": str(payload.get("zone", "SOCIAL PAVILION")),
                "habitable": bool(payload.get("habitable", True)),
                "wetRoom": bool(payload.get("wetRoom", False)),
                "sharedWetWall": payload.get("sharedWetWall"),
                "x": float(payload["x"]),
                "y": float(payload["y"]),
                "width": float(payload["width"]),
                "depth": float(payload["depth"]),
                "ceilingHeight": float(payload.get("ceilingHeight", 2.85)),
                "furniture": list(payload.get("furniture", [])),
            }
            spec.setdefault("rooms", []).append(room)
            return ok_response({"room_count": len(spec["rooms"]), "added": room}, revision=rev)

        if operation == "punch_door":
            door = {
                "id": str(payload.get("id", f"D-{len(spec.get('doors', [])) + 1:02d}")),
                "room": str(payload.get("room", "01")),
                "x": float(payload["x"]),
                "y": float(payload["y"]),
                "width": float(payload.get("width", 0.90)),
                "swingDeg": 90,
                "orientation": str(payload.get("orientation", "north")),
                "type": str(payload.get("type", "interior")),
            }
            spec.setdefault("doors", []).append(door)
            return ok_response({"door_count": len(spec["doors"]), "added": door}, revision=rev)

        if operation == "punch_window":
            win = {
                "id": str(payload.get("id", f"WIN-{len(spec.get('windows', [])) + 1:02d}")),
                "room": str(payload.get("room", "01")),
                "wall": str(payload.get("wall", "north")),
                "x1": float(payload["x1"]),
                "y1": float(payload["y1"]),
                "x2": float(payload["x2"]),
                "y2": float(payload["y2"]),
                "sill": float(payload.get("sill", 0.60)),
                "head": float(payload.get("head", 2.40)),
            }
            spec.setdefault("windows", []).append(win)
            return ok_response({"window_count": len(spec["windows"]), "added": win}, revision=rev)

        if operation == "add_stair":
            stair = {
                "id": str(payload.get("id", f"ST-{len(spec.get('stairs', [])) + 1:02d}")),
                "name": str(payload.get("name", "Staircase")),
                "riserMm": float(payload.get("riserMm", 155)),
                "treadMm": float(payload.get("treadMm", 295)),
                "riserCount": int(payload.get("riserCount", 20)),
                "widthM": float(payload.get("widthM", 1.20)),
                "x": float(payload["x"]),
                "y": float(payload["y"]),
            }
            spec.setdefault("stairs", []).append(stair)
            return ok_response({"stair_count": len(spec["stairs"]), "added": stair}, revision=rev)

        if operation == "place_furniture":
            item = str(payload.get("item") or payload.get("furniture_key"))
            if item not in FURNITURE_AND_FIXTURE_CATALOG:
                return error_response("E_UNKNOWN_FURNITURE", f"Unknown item '{item}'. Available: {list(FURNITURE_AND_FIXTURE_CATALOG.keys())}")
            rid = str(payload.get("room_id") or payload.get("room") or "01")
            for room in spec.get("rooms", []):
                if str(room["id"]) == rid:
                    room.setdefault("furniture", []).append({"item": item, "x": float(payload["x"]), "y": float(payload["y"])})
                    return ok_response({"room": rid, "placed": item}, revision=rev)
            return error_response("E_ROOM_NOT_FOUND", f"Room '{rid}' not found.")

        return error_response("E_INVALID_OPERATION", f"Unknown arch_element operation: {operation}")
