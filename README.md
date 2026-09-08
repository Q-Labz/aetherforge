# AetherForge

**Gaming development + motion graphics engine** that bridges **Reallusion Character Creator**, **Blender**, and **Godot 4** through a glTF-first pipeline.

```
Character Creator ──FBX/USD──► Blender (AetherForge Bridge)
                                      │
                          retarget · clean · motion graphics
                                      │
                                   glTF 2.0
                                      │
                                      ▼
                         Godot 4 Runtime (AetherForge)
                         games · cinematics · motion graphics
```

## What you get

| Layer | Role |
|---|---|
| **Character Creator bridge** | Export presets + docs for CC3/CC4 characters, clothes, and facial morphs |
| **Blender addon** | Import CC assets, retarget, author motion graphics, batch-export runtime glTF |
| **Godot 4 runtime** | Character player, animation library, motion-graphics timeline, scene staging |
| **Pipeline CLI** | Validate, convert, and package character packs for the engine |

## Quick start

### 1. Character Creator
Export your character as **FBX** (or USD) with the AetherForge preset in [`docs/character-creator.md`](docs/character-creator.md).

### 2. Blender
1. Install the addon from `blender/aetherforge_bridge/` (Edit → Preferences → Add-ons → Install from Disk / enable the folder as a legacy add-on, or zip the folder).
2. Enable **AetherForge Bridge**.
3. Use the **AetherForge** sidebar: *Import Character Creator* → author motion → *Export Runtime glTF*.

### 3. Godot
1. Open `godot/aetherforge/` in Godot 4.3+.
2. Drop exported `.glb` files into `assets/characters/`.
3. Run the **Character Stage** or **Motion Graphics** demo scenes.

### 4. CLI (optional)
```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
aetherforge validate path/to/character.glb
aetherforge pack path/to/character.glb --out ../godot/aetherforge/assets/characters/
```

## Repository layout

```
blender/aetherforge_bridge/   Blender 4.x addon
godot/aetherforge/            Godot 4 runtime + demos
pipeline/                     Python CLI + export presets
docs/                         Architecture and tool guides
examples/                     Sample manifests and tiny glTF fixtures
```

## Design principles

1. **glTF is the runtime contract** — everything ships as glTF 2.0 (+ extras metadata).
2. **Blender is the DCC hub** — Character Creator is the character source; Blender owns cleanup, motion graphics, and export.
3. **Godot is the interactive runtime** — games, realtime previews, and motion-graphics playback.
4. **Extras, not forks** — AetherForge metadata lives in glTF `extras.aetherforge` so assets stay portable.

## Status

Scaffold / MVP: import path, addon operators, Godot loaders, and CLI validators are in place. Extend with your animation libraries, Mixamo/CC retarget maps, and production export profiles.

## License

MIT — see [`LICENSE`](LICENSE).
