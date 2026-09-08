# AetherForge Pipeline CLI

Validate glTF sidecars and pack Character Creator / Blender exports into the Godot project.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
aetherforge validate ../examples/hello_character/hello_character.aetherforge.json
aetherforge pack /path/to/Hero.glb --out ../godot/aetherforge/assets/characters/
```
