# Examples

These fixtures are **metadata-only** samples of the AetherForge runtime contract.

- `hello_character/` — character sidecar shaped like a Character Creator → Blender export
- `hello_motion/` — motion graphics sidecar from the Blender MG rig

Validate with:

```bash
cd pipeline && pip install -e . && aetherforge validate ../examples/hello_character/hello_character.aetherforge.json
```
