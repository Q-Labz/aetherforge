import bpy
from bpy.types import Panel


class AETHERFORGE_PT_main(Panel):
    bl_label = "AetherForge"
    bl_idname = "AETHERFORGE_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherForge"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Character Creator", icon="OUTLINER_OB_ARMATURE")
        layout.operator("aetherforge.import_character_creator", icon="IMPORT")
        layout.operator("aetherforge.tag_active_character", icon="BOOKMARKS")

        layout.separator()
        layout.label(text="Motion Graphics", icon="CAMERA_DATA")
        layout.operator("aetherforge.add_motion_graphics_rig", icon="ANIM")

        layout.separator()
        layout.label(text="Runtime", icon="EXPORT")
        layout.operator("aetherforge.export_runtime_gltf", icon="FILE_TICK")

        active = context.view_layer.objects.active
        if active and "aetherforge" in active:
            box = layout.box()
            box.label(text=f"Active: {active.name}")
            meta = active.get("aetherforge")
            if isinstance(meta, dict):
                box.label(text=f"Kind: {meta.get('kind', '?')}")
                box.label(text=f"Skeleton: {meta.get('skeleton', '?')}")


classes = (AETHERFORGE_PT_main,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
