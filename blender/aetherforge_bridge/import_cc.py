from __future__ import annotations

import os

import bpy

from . import metadata


def import_character_creator(filepath: str, *, auto_apply_scale: bool = True) -> bpy.types.Object | None:
    """Import a Character Creator FBX or USD and return the armature (or root)."""
    filepath = bpy.path.abspath(filepath)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(filepath)

    ext = os.path.splitext(filepath)[1].lower()
    before = set(bpy.data.objects)

    if ext == ".fbx":
        bpy.ops.import_scene.fbx(
            filepath=filepath,
            automatic_bone_orientation=True,
            use_anim=True,
            ignore_leaf_bones=False,
        )
    elif ext in {".usd", ".usda", ".usdc", ".usdz"}:
        bpy.ops.wm.usd_import(filepath=filepath)
    else:
        raise ValueError(f"Unsupported Character Creator format: {ext}")

    imported = [obj for obj in bpy.data.objects if obj not in before]
    if not imported:
        return None

    root = _pick_root(imported)
    if auto_apply_scale and root is not None:
        _apply_scale_hierarchy(root)

    if root is not None:
        metadata.tag_character(root)
        root.name = root.name if root.name.lower().startswith("af_") else f"AF_{root.name}"
        root["aetherforge_source_path"] = filepath

    return root


def _pick_root(objects: list[bpy.types.Object]) -> bpy.types.Object | None:
    armatures = [o for o in objects if o.type == "ARMATURE"]
    if armatures:
        # Prefer an armature that has no armature parent.
        for arm in armatures:
            if arm.parent is None or arm.parent.type != "ARMATURE":
                return arm
        return armatures[0]

    roots = [o for o in objects if o.parent is None]
    return roots[0] if roots else objects[0]


def _apply_scale_hierarchy(root: bpy.types.Object) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    root.select_set(True)
    bpy.context.view_layer.objects.active = root
    # Select children so Apply Object Transform covers the character pack.
    for child in root.children_recursive:
        child.select_set(True)
    try:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    except RuntimeError:
        # Some linked/proxy objects cannot be applied; ignore quietly.
        pass
