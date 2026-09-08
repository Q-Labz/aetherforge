bl_info = {
    "name": "AetherForge Bridge",
    "author": "AetherForge",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > AetherForge",
    "description": "Character Creator import, motion graphics authoring, and Godot-ready glTF export",
    "category": "Import-Export",
    "doc_url": "https://github.com/Q-Labz/aetherforge",
}

from . import operators, prefs, ui


def register():
    prefs.register()
    operators.register()
    ui.register()


def unregister():
    ui.unregister()
    operators.unregister()
    prefs.unregister()


if __name__ == "__main__":
    register()
