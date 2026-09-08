from __future__ import annotations

import bpy
from mathutils import Euler, Vector

from . import metadata


def add_motion_graphics_rig(
    context,
    *,
    fps: int = 24,
    duration: float = 4.0,
) -> bpy.types.Object:
    """Create a camera + title empty + marker collection for motion graphics."""
    scene = context.scene
    scene.render.fps = fps

    collection = bpy.data.collections.new("AF_MotionGraphics")
    scene.collection.children.link(collection)

    root = bpy.data.objects.new("AF_MG_Root", None)
    root.empty_display_type = "PLAIN_AXES"
    collection.objects.link(root)

    camera_data = bpy.data.cameras.new("AF_MG_Camera")
    camera_data.lens = 35
    camera = bpy.data.objects.new("AF_MG_Camera", camera_data)
    camera.location = Vector((0.0, -4.5, 1.6))
    camera.rotation_euler = Euler((1.3, 0.0, 0.0), "XYZ")
    camera.parent = root
    collection.objects.link(camera)
    scene.camera = camera

    title = bpy.data.objects.new("AF_MG_Title", None)
    title.empty_display_type = "CUBE"
    title.empty_display_size = 0.35
    title.location = Vector((0.0, 0.0, 2.0))
    title.parent = root
    collection.objects.link(title)

    fx = bpy.data.objects.new("AF_MG_FX", None)
    fx.empty_display_type = "SPHERE"
    fx.empty_display_size = 0.25
    fx.location = Vector((0.8, 0.0, 1.2))
    fx.parent = root
    collection.objects.link(fx)

    _seed_camera_move(camera, duration=duration, fps=fps)
    _seed_title_pop(title, duration=duration, fps=fps)
    _add_timeline_markers(scene, duration=duration, fps=fps)

    metadata.tag_motion_graphics(
        root,
        fps=fps,
        duration=duration,
        layers=["camera", "titles", "fx"],
    )
    return root


def _frame(seconds: float, fps: int) -> int:
    return max(1, int(round(seconds * fps)))


def _ensure_action(obj: bpy.types.Object, name: str) -> bpy.types.Action:
    if obj.animation_data is None:
        obj.animation_data_create()
    action = bpy.data.actions.new(name=name)
    obj.animation_data.action = action
    return action


def _seed_camera_move(camera: bpy.types.Object, *, duration: float, fps: int) -> None:
    action = _ensure_action(camera, "AF_MG_CameraMove")
    start, mid, end = 1, _frame(duration * 0.5, fps), _frame(duration, fps)
    # Location: slow push-in.
    for frame, loc in (
        (start, (0.0, -4.5, 1.6)),
        (mid, (0.15, -3.6, 1.55)),
        (end, (0.0, -3.0, 1.5)),
    ):
        camera.location = Vector(loc)
        camera.keyframe_insert(data_path="location", frame=frame)
    action.use_fake_user = True


def _seed_title_pop(title: bpy.types.Object, *, duration: float, fps: int) -> None:
    action = _ensure_action(title, "AF_MG_TitlePop")
    start, hit, end = 1, _frame(0.35, fps), _frame(duration, fps)
    for frame, scale in ((start, 0.01), (hit, 1.0), (end, 1.0)):
        title.scale = Vector((scale, scale, scale))
        title.keyframe_insert(data_path="scale", frame=frame)
    action.use_fake_user = True


def _add_timeline_markers(scene: bpy.types.Scene, *, duration: float, fps: int) -> None:
    markers = [
        ("AF_MARK_INTRO", 0.0),
        ("AF_MARK_BEAT", duration * 0.5),
        ("AF_MARK_OUTRO", duration * 0.9),
    ]
    existing = {m.name for m in scene.timeline_markers}
    for name, seconds in markers:
        if name in existing:
            continue
        scene.timeline_markers.new(name, frame=_frame(seconds, fps))
