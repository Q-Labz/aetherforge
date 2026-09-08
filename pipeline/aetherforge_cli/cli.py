from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import validate as validate_mod


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aetherforge", description="AetherForge asset pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="Validate a glTF sidecar or .aetherforge.json")
    p_validate.add_argument("path", type=Path)

    p_pack = sub.add_parser("pack", help="Copy a .glb (+ sidecar) into a Godot assets folder")
    p_pack.add_argument("glb", type=Path)
    p_pack.add_argument("--out", type=Path, required=True, help="Target assets/characters or motion_graphics dir")
    p_pack.add_argument("--name", type=str, default="", help="Pack folder name (default: glb stem)")
    p_pack.add_argument("--kind", choices=("character", "motion_graphics", "auto"), default="auto")

    p_init = sub.add_parser("init-sidecar", help="Write a starter .aetherforge.json next to a glb")
    p_init.add_argument("glb", type=Path)
    p_init.add_argument("--kind", choices=("character", "motion_graphics", "prop"), default="character")

    args = parser.parse_args(argv)

    if args.command == "validate":
        return _cmd_validate(args.path)
    if args.command == "pack":
        return _cmd_pack(args.glb, args.out, args.name, args.kind)
    if args.command == "init-sidecar":
        return _cmd_init_sidecar(args.glb, args.kind)
    return 1


def _cmd_validate(path: Path) -> int:
    try:
        report = validate_mod.validate_path(path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if report["ok"]:
        print(f"OK  {path}")
        for line in report.get("notes", []):
            print(f"  - {line}")
        return 0
    print(f"FAIL  {path}", file=sys.stderr)
    for err in report.get("errors", []):
        print(f"  - {err}", file=sys.stderr)
    return 1


def _cmd_pack(glb: Path, out_root: Path, name: str, kind: str) -> int:
    if not glb.is_file():
        print(f"ERROR: missing glb {glb}", file=sys.stderr)
        return 2
    pack_name = name or glb.stem
    sidecar = glb.parent / f"{glb.stem}.aetherforge.json"

    resolved_kind = kind
    if kind == "auto":
        resolved_kind = "character"
        if sidecar.is_file():
            data = json.loads(sidecar.read_text(encoding="utf-8"))
            af = data.get("aetherforge", data)
            resolved_kind = "motion_graphics" if af.get("kind") == "motion_graphics" else "character"

    target = out_root / pack_name
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(glb, target / glb.name)
    if sidecar.is_file():
        shutil.copy2(sidecar, target / f"{glb.stem}.aetherforge.json")
    else:
        _write_sidecar(target / f"{glb.stem}.aetherforge.json", resolved_kind if resolved_kind != "auto" else "character")

    print(f"Packed {pack_name} → {target}")
    return 0


def _cmd_init_sidecar(glb: Path, kind: str) -> int:
    path = glb.parent / f"{glb.stem}.aetherforge.json"
    _write_sidecar(path, kind)
    print(f"Wrote {path}")
    return 0


def _write_sidecar(path: Path, kind: str) -> None:
    if kind == "motion_graphics":
        payload = {
            "aetherforge": {
                "version": 1,
                "kind": "motion_graphics",
                "motion_graphics": {
                    "fps": 24,
                    "duration": 4.0,
                    "layers": ["camera", "titles", "fx"],
                    "markers": [
                        {"name": "AF_MARK_INTRO", "time": 0.0},
                        {"name": "AF_MARK_BEAT", "time": 2.0},
                        {"name": "AF_MARK_OUTRO", "time": 3.6},
                    ],
                },
            }
        }
    elif kind == "prop":
        payload = {"aetherforge": {"version": 1, "kind": "prop"}}
    else:
        payload = {
            "aetherforge": {
                "version": 1,
                "kind": "character",
                "source": {"character_creator": "4.x", "blender": "4.x"},
                "skeleton": "cc_standard",
                "morphs": [],
                "clips": [{"name": "Idle", "loop": True}],
            }
        }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
