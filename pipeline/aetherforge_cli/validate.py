from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_VERSION = 1
ALLOWED_KINDS = {"character", "prop", "motion_graphics"}


def validate_path(path: Path) -> dict[str, Any]:
    path = Path(path)
    if path.suffix.lower() in {".glb", ".gltf"}:
        sidecar = path.parent / f"{path.stem}.aetherforge.json"
        if not sidecar.is_file():
            return {"ok": False, "errors": [f"Missing sidecar next to glTF: {sidecar.name}"]}
        path = sidecar

    if not path.is_file():
        return {"ok": False, "errors": [f"File not found: {path}"]}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"ok": False, "errors": [f"Invalid JSON: {exc}"]}

    return validate_document(data)


def validate_document(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    notes: list[str] = []

    af = data.get("aetherforge", data)
    if not isinstance(af, dict):
        return {"ok": False, "errors": ["Root aetherforge object must be a dictionary"]}

    version = af.get("version")
    if version != REQUIRED_VERSION:
        errors.append(f"version must be {REQUIRED_VERSION}, got {version!r}")

    kind = af.get("kind")
    if kind not in ALLOWED_KINDS:
        errors.append(f"kind must be one of {sorted(ALLOWED_KINDS)}, got {kind!r}")

    if kind == "character":
        if "skeleton" not in af:
            errors.append("character assets require skeleton")
        clips = af.get("clips", [])
        if not isinstance(clips, list):
            errors.append("clips must be a list")
        else:
            notes.append(f"{len(clips)} clip stub(s)")
        morphs = af.get("morphs", [])
        if isinstance(morphs, list):
            notes.append(f"{len(morphs)} morph(s)")

    if kind == "motion_graphics":
        mg = af.get("motion_graphics")
        if not isinstance(mg, dict):
            errors.append("motion_graphics kind requires motion_graphics object")
        else:
            if "fps" not in mg or "duration" not in mg:
                errors.append("motion_graphics requires fps and duration")
            else:
                notes.append(f"{mg.get('fps')} fps · {mg.get('duration')}s")

    return {"ok": not errors, "errors": errors, "notes": notes}
