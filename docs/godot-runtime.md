# Godot 4 Runtime

Open `godot/aetherforge/` in **Godot 4.3+**.

## Scenes

| Scene | Purpose |
|---|---|
| `scenes/main.tscn` | Boot menu → stage / motion graphics |
| `scenes/character_stage.tscn` | Load a character glTF and play clips |
| `scenes/motion_graphics_demo.tscn` | Scrub / play MG timelines |

## Core scripts

| Script | Role |
|---|---|
| `scripts/aetherforge/character_actor.gd` | Instantiates glTF, binds skeleton + AnimationPlayer |
| `scripts/aetherforge/gltf_meta.gd` | Reads `extras.aetherforge` |
| `scripts/aetherforge/motion_graphics_player.gd` | Timeline scrub, layer mute, markers |
| `scripts/aetherforge/asset_library.gd` | Scans `assets/characters/` |

## Drop-in characters

```
godot/aetherforge/assets/characters/
  Hero_A/
    Hero_A.glb
    thumb.png          # optional
```

The stage auto-lists folders that contain a `.glb`.

## Motion graphics

Export MG scenes from Blender as glTF. The player looks for:

- Animation libraries / clips
- `extras.aetherforge.motion_graphics` (fps, duration, layers)
- Marker tracks named `AF_MARK_*` (converted to signals)

## Input (Character Stage)

| Key | Action |
|---|---|
| `1`–`9` | Play clip by index |
| `Space` | Toggle pause |
| `R` | Reset to idle / first clip |
| `Esc` | Back to main |

## Extending for games

`CharacterActor` is intentionally thin — wrap it in your gameplay controller (movement, combat, dialogue) while keeping animation playback here.
