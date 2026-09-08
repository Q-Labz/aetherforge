# Character Creator → AetherForge

Supported: **Reallusion Character Creator 3 / 4** (and AccuRIG-ready characters).

## Export preset (recommended)

In Character Creator:

1. **File → Export → FBX (Clothed Character)** (or **USD** if you prefer Blender's USD importer).
2. Use these settings:

| Setting | Value |
|---|---|
| Target Tool Preset | **Blender** (or Custom) |
| Embed Textures | On |
| Mesh | Embed + Merge materials when possible |
| Skeleton | **Export with T-Pose** baseline preferred |
| Facial Profile | Export morphs / expression keys you need at runtime |
| Hair / Cloth | Include if intended for realtime (keep poly budget in mind) |
| Scale | **Meters** (1 unit = 1 m) |

3. Save next to a `manifest.json` (optional but recommended):

```json
{
  "name": "Hero_A",
  "source": "character_creator",
  "version": "4.5",
  "fbx": "Hero_A.fbx",
  "textures": "./textures",
  "notes": "Game-ready body + face morphs"
}
```

## What AetherForge expects

- Single root armature (CC standard humanoid).
- Morph targets named consistently (CC facial keys are fine).
- Textures either embedded or in a sibling `textures/` folder.
- No cinematic-only Alembic caches unless you also ship a realtime mesh.

## Import into Blender

1. Enable **AetherForge Bridge**.
2. Sidebar → **AetherForge → Import Character Creator**.
3. Pick the `.fbx` (or `.usd`).
4. The addon will:
   - Import the file
   - Tag the armature with `aetherforge.kind = character`
   - Apply a light cleanup (apply scale, rename root, ensure rest pose)
   - Open the Motion Graphics panel for optional cinematic setup

## Export for Godot

1. Select the character root (or leave empty to export the active collection).
2. **AetherForge → Export Runtime glTF**.
3. Output `.glb` into `godot/aetherforge/assets/characters/<Name>/`.
4. The export writes `extras.aetherforge` automatically.

## Clothes & accessories

Export outfits as separate FBX files parented to the same skeleton, or as mesh slots on the same character. Tag props with `kind: "prop"` in Blender before export.

## Facial animation

- Prefer **morph targets** for realtime Godot playback.
- Use Alembic / MDD only for offline Blender motion-graphics renders.
- List active morph names under `extras.aetherforge.morphs`.

## Troubleshooting

| Issue | Fix |
|---|---|
| Giant / tiny character | Re-export in meters; in Blender apply scale before export |
| Missing textures | Embed textures in FBX or keep relative `textures/` paths |
| Twisted bones in Godot | Use the Blender → Godot bone map / rest-pose fix in the addon |
| Morphs missing | Enable facial morph export in CC; verify shape keys in Blender |
