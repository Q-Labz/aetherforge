class_name CharacterActor
extends Node3D
## Loads a Character Creator → Blender → glTF character and plays clips.

signal clip_changed(clip_name: String)
signal loaded(meta: Dictionary)

var meta: Dictionary = {}
var _instance: Node = null
var _animation_player: AnimationPlayer = null
var _clip_names: PackedStringArray = []


func load_character(glb_path: String, sidecar_path: String = "") -> Error:
	clear()
	if not ResourceLoader.exists(glb_path):
		push_error("Character glTF not found: %s" % glb_path)
		return ERR_FILE_NOT_FOUND

	var packed: PackedScene = load(glb_path)
	if packed == null:
		return ERR_CANT_OPEN

	_instance = packed.instantiate()
	add_child(_instance)

	if sidecar_path == "":
		sidecar_path = GltfMeta.find_sidecar_for_glb(glb_path)
	meta = GltfMeta.from_sidecar(sidecar_path)
	if meta.is_empty():
		meta = {"kind": "character", "clips": []}

	_animation_player = _find_animation_player(_instance)
	_clip_names = _gather_clips()
	loaded.emit(meta)
	if not _clip_names.is_empty():
		play_clip(_clip_names[0])
	return OK


func clear() -> void:
	if _instance != null:
		_instance.queue_free()
		_instance = null
	_animation_player = null
	_clip_names = []
	meta = {}


func get_clip_names() -> PackedStringArray:
	return _clip_names


func play_clip(clip_name: String, custom_blend: float = 0.2) -> void:
	if _animation_player == null:
		return
	if not _animation_player.has_animation(clip_name):
		# Godot 4 may nest library/clip as "lib/clip".
		var resolved := _resolve_clip(clip_name)
		if resolved == "":
			push_warning("Missing clip: %s" % clip_name)
			return
		clip_name = resolved
	_animation_player.play(clip_name, custom_blend)
	clip_changed.emit(clip_name)


func play_clip_index(index: int) -> void:
	if index < 0 or index >= _clip_names.size():
		return
	play_clip(_clip_names[index])


func toggle_pause() -> void:
	if _animation_player == null:
		return
	_animation_player.paused = not _animation_player.paused


func reset_to_first() -> void:
	if _clip_names.is_empty():
		return
	play_clip(_clip_names[0])


func _gather_clips() -> PackedStringArray:
	var from_meta := GltfMeta.clip_names(meta)
	if _animation_player == null:
		return from_meta
	var from_player: PackedStringArray = []
	for anim_name in _animation_player.get_animation_list():
		from_player.append(anim_name)
	if from_meta.is_empty():
		return from_player
	# Prefer meta order, keep only clips that exist when possible.
	var ordered: PackedStringArray = []
	for name in from_meta:
		var resolved := _resolve_clip(name)
		ordered.append(resolved if resolved != "" else name)
	for name in from_player:
		if not ordered.has(name):
			ordered.append(name)
	return ordered


func _resolve_clip(clip_name: String) -> String:
	if _animation_player == null:
		return ""
	if _animation_player.has_animation(clip_name):
		return clip_name
	for anim_name in _animation_player.get_animation_list():
		if str(anim_name).ends_with("/" + clip_name) or str(anim_name) == clip_name:
			return str(anim_name)
	return ""


func _find_animation_player(root: Node) -> AnimationPlayer:
	if root is AnimationPlayer:
		return root
	for child in root.get_children():
		var found := _find_animation_player(child)
		if found != null:
			return found
	return null
