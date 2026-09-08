# AetherForge Bridge — Blender Addon

Installable Blender 4.x addon that:

1. Imports Character Creator FBX/USD
2. Tags assets with AetherForge metadata
3. Authors simple motion-graphics layers (camera, titles, markers)
4. Exports runtime glTF with `extras.aetherforge`

## Install

### Option A — Development (symlink)

```bash
# Linux
ln -s "$(pwd)/blender/aetherforge_bridge" \
  ~/.config/blender/4.2/scripts/addons/aetherforge_bridge
```

Then enable **AetherForge Bridge** in Preferences → Add-ons.

### Option B — Zip install

```bash
cd blender
zip -r aetherforge_bridge.zip aetherforge_bridge
```

Edit → Preferences → Add-ons → Install → pick the zip.

## UI

**3D Viewport → Sidebar (N) → AetherForge**

- **Import Character Creator** — FBX/USD import + tagging
- **Add Motion Graphics Rig** — camera + title empty + marker collection
- **Bake Motion Pass** — prepares animation for export
- **Export Runtime glTF** — glTF 2.0 `.glb` with extras

## Operators (Python IDs)

| ID | Purpose |
|---|---|
| `aetherforge.import_character_creator` | CC import |
| `aetherforge.add_motion_graphics_rig` | MG scaffold |
| `aetherforge.tag_active_character` | Write metadata on selection |
| `aetherforge.export_runtime_gltf` | Runtime export |

## Preferences

- Default export directory
- Default skeleton profile (`cc_standard` / `godot_humanoid`)
- Auto-apply scale on import
