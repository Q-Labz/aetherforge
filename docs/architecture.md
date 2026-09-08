# Architecture

AetherForge is a **pipeline engine**, not a monolithic renderer. Each tool keeps its strength; AetherForge standardizes the handoff.

## Data flow

```
┌─────────────────────┐
│ Character Creator   │  authoring: body, face, clothes, skin
│ (Reallusion CC3/4)  │
└──────────┬──────────┘
           │ FBX / USD (+ optional Alembic facial)
           ▼
┌─────────────────────┐
│ Blender             │  hub: retarget, materials, motion graphics,
│ AetherForge Bridge  │  cameras, lighting, cinematic beats
└──────────┬──────────┘
           │ glTF 2.0 (+ extras.aetherforge)
           ▼
┌─────────────────────┐
│ Godot 4 Runtime     │  games, interactive stage, motion-graphics
│ AetherForge         │  timeline playback, character controller
└─────────────────────┘
```

## Runtime contract (`extras.aetherforge`)

Every exported glTF should carry:

```json
{
  "aetherforge": {
    "version": 1,
    "kind": "character" | "prop" | "motion_graphics",
    "source": {
      "character_creator": "4.x",
      "blender": "4.x"
    },
    "skeleton": "cc_standard" | "godot_humanoid" | "custom",
    "morphs": ["Eye_Blink_L", "Mouth_Smile"],
    "clips": [
      { "name": "Idle", "loop": true },
      { "name": "Walk", "loop": true }
    ],
    "motion_graphics": {
      "fps": 24,
      "duration": 4.0,
      "layers": ["camera", "titles", "fx"]
    }
  }
}
```

## Modules

| Module | Language | Responsibility |
|---|---|---|
| `blender/aetherforge_bridge` | Python (bpy) | CC import, MG authoring, glTF export |
| `godot/aetherforge` | GDScript | Load extras, play clips, MG timeline |
| `pipeline` | Python | Validate extras, pack assets into Godot folders |

## Motion graphics model

Motion graphics in AetherForge are **scene-graph animations** authored in Blender (cameras, empties, text, lights, procedural modifiers) and exported as:

1. Animated transforms on nodes (standard glTF animation)
2. Optional `motion_graphics.layers` metadata for Godot timeline UI
3. Separate `.json` beat sheet when you need marker-driven cuts

Godot's `MotionGraphicsPlayer` reads the glTF animations and exposes layer solo/mute, scrubbing, and marker callbacks for game events.

## Character Creator → Godot bone map

Default map assumes CC standard humanoid → Godot `Skeleton3D` names used by the runtime's `CharacterActor`. Custom maps live in `pipeline/presets/bone_maps/`.

## Extending

- Add Mixamo / Rokoko retarget operators in the Blender addon.
- Add facial ARKit / CC expression drivers via morph target extras.
- Swap Godot for another runtime by consuming the same glTF contract.
