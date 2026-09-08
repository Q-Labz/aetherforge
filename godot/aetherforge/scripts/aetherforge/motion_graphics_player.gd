class_name MotionGraphicsPlayer
extends Node3D
## Plays Blender-authored motion graphics glTF with scrubbing and marker signals.

signal marker_reached(marker_name: String)
signal playback_finished
signal time_changed(seconds: float)

var meta: Dictionary = {}
var duration: float = 4.0
var fps: int = 24
var layers: PackedStringArray = []

var _instance: Node = null
var _animation_players: Array[AnimationPlayer] = []
var _playing: bool = false
var _time: float = 0.0
var _markers: Array[Dictionary] = []
var _fired_markers: Dictionary = {}


func load_scene(glb_path: String, sidecar_path: String = "") -> Error:
	clear()
	if not ResourceLoader.exists(glb_path):
		return ERR_FILE_NOT_FOUND
	var packed: PackedScene = load(glb_path)
	if packed == null:
		return ERR_CANT_OPEN
	_instance = packed.instantiate()
	add_child(_instance)

	if sidecar_path == "":
		sidecar_path = GltfMeta.find_sidecar_for_glb(glb_path)
	meta = GltfMeta.from_sidecar(sidecar_path)
	var mg := GltfMeta.motion_graphics(meta)
	fps = int(mg.get("fps", 24))
	duration = float(mg.get("duration", 4.0))
	layers = PackedStringArray(mg.get("layers", ["camera", "titles", "fx"]))

	_animation_players = _collect_animation_players(_instance)
	_markers = _collect_markers_from_meta(mg)
	_play_all_from_start()
	pause()
	return OK


func clear() -> void:
	if _instance != null:
		_instance.queue_free()
		_instance = null
	_animation_players.clear()
	_markers.clear()
	_fired_markers.clear()
	_time = 0.0
	_playing = false


func play() -> void:
	_playing = true
	for player in _animation_players:
		player.paused = false


func pause() -> void:
	_playing = false
	for player in _animation_players:
		player.paused = true


func toggle() -> void:
	if _playing:
		pause()
	else:
		play()


func seek(seconds: float) -> void:
	_time = clampf(seconds, 0.0, duration)
	_fired_markers.clear()
	for player in _animation_players:
		for anim_name in player.get_animation_list():
			player.play(anim_name)
			player.seek(_time, true)
			player.paused = not _playing
	time_changed.emit(_time)


func _process(delta: float) -> void:
	if not _playing:
		return
	_time += delta
	if _time >= duration:
		_time = duration
		pause()
		playback_finished.emit()
	_emit_markers()
	time_changed.emit(_time)


func _play_all_from_start() -> void:
	for player in _animation_players:
		var list := player.get_animation_list()
		if list.is_empty():
			continue
		player.play(list[0])
		player.seek(0.0, true)


func _emit_markers() -> void:
	for marker in _markers:
		var name := str(marker.get("name", ""))
		var at := float(marker.get("time", 0.0))
		if _time >= at and not _fired_markers.has(name):
			_fired_markers[name] = true
			marker_reached.emit(name)


func _collect_animation_players(root: Node) -> Array[AnimationPlayer]:
	var found: Array[AnimationPlayer] = []
	if root is AnimationPlayer:
		found.append(root)
	for child in root.get_children():
		found.append_array(_collect_animation_players(child))
	return found


func _collect_markers_from_meta(mg: Dictionary) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	# Default beats if none provided.
	out.append({"name": "AF_MARK_INTRO", "time": 0.0})
	out.append({"name": "AF_MARK_BEAT", "time": duration * 0.5})
	out.append({"name": "AF_MARK_OUTRO", "time": duration * 0.9})
	var custom: Variant = mg.get("markers", [])
	if typeof(custom) == TYPE_ARRAY:
		for item in custom:
			if typeof(item) == TYPE_DICTIONARY and item.has("name"):
				out.append(item)
	return out
