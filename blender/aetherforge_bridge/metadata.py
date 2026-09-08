"""Shared AetherForge metadata helpers for Blender objects / scenes."""

from __future__ import annotations

import json
from typing import Any

AF_KEY = "aetherforge"
AF_VERSION = 1


def get_prefs(context):
    return context.preferences.addons[__package__.split(".")[0]].preferences


def ensure_dict(obj) -> dict[str, Any]:
    raw = obj.get(AF_KEY)
    if isinstance(raw, dict):
        return dict(raw)
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    return {"version": AF_VERSION}


def write_meta(obj, meta: dict[str, Any]) -> None:
    payload = dict(meta)
    payload.setdefault("version", AF_VERSION)
    obj[AF_KEY] = payload


def tag_character(obj, *, source: str = "character_creator", skeleton: str = "cc_standard") -> None:
    meta = ensure_dict(obj)
    meta.update(
        {
            "version": AF_VERSION,
            "kind": "character",
            "source": {"character_creator": source, "blender": "4.x"},
            "skeleton": skeleton,
            "morphs": _collect_morph_names(obj),
            "clips": _collect_clip_stubs(obj),
        }
    )
    write_meta(obj, meta)


def tag_motion_graphics(obj, *, fps: int = 24, duration: float = 4.0, layers: list[str] | None = None) -> None:
    meta = ensure_dict(obj)
    meta.update(
        {
            "version": AF_VERSION,
            "kind": "motion_graphics",
            "motion_graphics": {
                "fps": fps,
                "duration": duration,
                "layers": layers or ["camera", "titles", "fx"],
            },
        }
    )
    write_meta(obj, meta)


def _collect_morph_names(obj) -> list[str]:
    names: list[str] = []
    for child in obj.children_recursive:
        data = getattr(child, "data", None)
        shape_keys = getattr(data, "shape_keys", None)
        if not shape_keys:
            continue
        for key in shape_keys.key_blocks:
            if key.name != "Basis" and key.name not in names:
                names.append(key.name)
    return names


def _collect_clip_stubs(obj) -> list[dict[str, Any]]:
    clips: list[dict[str, Any]] = []
    action_names: set[str] = set()
    if obj.animation_data and obj.animation_data.action:
        action_names.add(obj.animation_data.action.name)
    for child in obj.children_recursive:
        ad = getattr(child, "animation_data", None)
        if ad and ad.action:
            action_names.add(ad.action.name)
    for name in sorted(action_names):
        clips.append({"name": name, "loop": name.lower() in {"idle", "walk", "run"}})
    if not clips:
        clips = [{"name": "Idle", "loop": True}]
    return clips


def build_export_extras(root) -> dict[str, Any]:
    meta = ensure_dict(root)
    meta.setdefault("version", AF_VERSION)
    meta.setdefault("kind", "character")
    if meta.get("kind") == "character":
        meta["morphs"] = _collect_morph_names(root)
        meta["clips"] = _collect_clip_stubs(root)
    return {AF_KEY: meta}
