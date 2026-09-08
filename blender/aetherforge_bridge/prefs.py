import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import AddonPreferences


class AetherForgePreferences(AddonPreferences):
    bl_idname = __package__

    export_dir: StringProperty(
        name="Default Export Directory",
        subtype="DIR_PATH",
        default="//exports/",
        description="Default folder for runtime glTF exports",
    )

    skeleton_profile: EnumProperty(
        name="Skeleton Profile",
        items=(
            ("cc_standard", "Character Creator Standard", "Keep CC bone names"),
            ("godot_humanoid", "Godot Humanoid", "Prefer Godot-friendly naming"),
            ("custom", "Custom", "Do not remapping; use as-is"),
        ),
        default="cc_standard",
    )

    auto_apply_scale: BoolProperty(
        name="Auto Apply Scale on Import",
        default=True,
    )

    default_fps: IntProperty(
        name="Motion Graphics FPS",
        default=24,
        min=1,
        max=120,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_dir")
        layout.prop(self, "skeleton_profile")
        layout.prop(self, "auto_apply_scale")
        layout.prop(self, "default_fps")


classes = (AetherForgePreferences,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
