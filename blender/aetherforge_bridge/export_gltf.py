from __future__ import annotations

import json
import os

import bpy

from . import metadata


def export_runtime_gltf(
    context,
    filepath: str,
    *,
    root: bpy.types.Object | None = None,
) -> str:
    """Export selection (or whole scene) as glTF with AetherForge extras sidecar metadata."""
    filepath = bpy.path.abspath(filepath)
    if not filepath.lower().endswith((".glb", ".gltf")):
        filepath += ".glb"

    out_dir = os.path.dirname(filepath)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    root = root or context.view_layer.objects.active
    extras = metadata.build_export_extras(root) if root else {"aetherforge": {"version": 1, "kind": "prop"}}

    # Stash extras on the root custom properties so the glTF exporter embeds them.
    if root is not None:
        root["aetherforge"] = extras["aetherforge"]

    selected = list(context.selected_objects)
    if root is not None and root not in selected:
        bpy.ops.object.select_all(action="DESELECT")
        root.select_set(True)
        for child in root.children_recursive:
            child.select_set(True)
        context.view_layer.objects.active = root

    export_format = "GLB" if filepath.lower().endswith(".glb") else "GLTF_SEPARATE"
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=export_format,
        use_selection=bool(context.selected_objects),
        export_animations=True,
        export_skins=True,
        export_morph=True,
        export_apply=False,
        export_extras=True,
        export_yup=True,
    )

    # Sidecar JSON for pipeline tools that prefer not to parse binary glTF.
    sidecar = os.path.splitext(filepath)[0] + ".aetherforge.json"
    with open(sidecar, "w", encoding="utf-8") as handle:
        json.dump(extras, handle, indent=2)

    # Restore selection loosely.
    if selected:
        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected:
            try:
                obj.select_set(True)
            except ReferenceError:
                pass

    return filepath
