from __future__ import annotations

import bpy
from bpy.props import FloatProperty, StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper, ImportHelper

from . import export_gltf, import_cc, metadata, motion_graphics


def _addon_prefs(context):
    addon = context.preferences.addons.get(__package__)
    if addon is None:
        # When loaded as package submodule, preferences live on package root.
        root = __package__.split(".")[0]
        addon = context.preferences.addons.get(root)
    return addon.preferences if addon else None


class AETHERFORGE_OT_import_character_creator(Operator, ImportHelper):
    bl_idname = "aetherforge.import_character_creator"
    bl_label = "Import Character Creator"
    bl_description = "Import a Reallusion Character Creator FBX or USD and tag it for AetherForge"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".*"
    filter_glob: StringProperty(default="*.fbx;*.usd;*.usda;*.usdc;*.usdz", options={"HIDDEN"})

    def execute(self, context):
        prefs = _addon_prefs(context)
        auto_scale = True if prefs is None else prefs.auto_apply_scale
        try:
            root = import_cc.import_character_creator(self.filepath, auto_apply_scale=auto_scale)
        except Exception as exc:  # noqa: BLE001 - surface to Blender UI
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        if root is None:
            self.report({"WARNING"}, "Import finished but no root object was found")
            return {"CANCELLED"}

        if prefs is not None:
            metadata.tag_character(root, skeleton=prefs.skeleton_profile)

        self.report({"INFO"}, f"Imported Character Creator asset: {root.name}")
        return {"FINISHED"}


class AETHERFORGE_OT_add_motion_graphics_rig(Operator):
    bl_idname = "aetherforge.add_motion_graphics_rig"
    bl_label = "Add Motion Graphics Rig"
    bl_description = "Create camera, title, FX empties, seeded animation, and timeline markers"
    bl_options = {"REGISTER", "UNDO"}

    duration: FloatProperty(name="Duration (s)", default=4.0, min=0.5, max=120.0)

    def execute(self, context):
        prefs = _addon_prefs(context)
        fps = 24 if prefs is None else prefs.default_fps
        root = motion_graphics.add_motion_graphics_rig(context, fps=fps, duration=self.duration)
        context.view_layer.objects.active = root
        self.report({"INFO"}, f"Motion graphics rig created: {root.name}")
        return {"FINISHED"}


class AETHERFORGE_OT_tag_active_character(Operator):
    bl_idname = "aetherforge.tag_active_character"
    bl_label = "Tag Active as Character"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.view_layer.objects.active
        if obj is None:
            self.report({"ERROR"}, "No active object")
            return {"CANCELLED"}
        prefs = _addon_prefs(context)
        skeleton = "cc_standard" if prefs is None else prefs.skeleton_profile
        metadata.tag_character(obj, skeleton=skeleton)
        self.report({"INFO"}, f"Tagged {obj.name} as AetherForge character")
        return {"FINISHED"}


class AETHERFORGE_OT_export_runtime_gltf(Operator, ExportHelper):
    bl_idname = "aetherforge.export_runtime_gltf"
    bl_label = "Export Runtime glTF"
    bl_description = "Export Godot-ready glTF/GLB with AetherForge extras and sidecar JSON"
    bl_options = {"REGISTER"}

    filename_ext = ".glb"
    filter_glob: StringProperty(default="*.glb;*.gltf", options={"HIDDEN"})

    def invoke(self, context, event):
        prefs = _addon_prefs(context)
        if prefs is not None and prefs.export_dir:
            self.filepath = bpy.path.abspath(prefs.export_dir)
            if not self.filepath.endswith(("/", "\\")):
                self.filepath += "/"
            active = context.view_layer.objects.active
            name = active.name if active else "aetherforge_asset"
            self.filepath = self.filepath + f"{name}.glb"
        return super().invoke(context, event)

    def execute(self, context):
        try:
            path = export_gltf.export_runtime_gltf(context, self.filepath)
        except Exception as exc:  # noqa: BLE001
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Exported runtime glTF: {path}")
        return {"FINISHED"}


classes = (
    AETHERFORGE_OT_import_character_creator,
    AETHERFORGE_OT_add_motion_graphics_rig,
    AETHERFORGE_OT_tag_active_character,
    AETHERFORGE_OT_export_runtime_gltf,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
