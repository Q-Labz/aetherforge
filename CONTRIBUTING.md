# CONTRIBUTING

## Pipeline

1. Author characters in **Character Creator** using the export preset in `docs/character-creator.md`.
2. Import into **Blender** with **AetherForge Bridge**.
3. Author gameplay animations and/or motion graphics.
4. Export runtime `.glb` + `.aetherforge.json`.
5. Pack into Godot:
   ```bash
   aetherforge pack Hero.glb --out godot/aetherforge/assets/characters/
   ```
6. Open `godot/aetherforge` in Godot 4.3+ and run **Character Stage** or **Motion Graphics**.

## Development notes

- Keep runtime metadata in `extras.aetherforge` / sidecar JSON — do not invent parallel formats.
- Prefer additive Godot scripts over rewriting imported scenes.
- Blender addon targets Blender 4.0+.
