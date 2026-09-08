extends Node3D
## Demo scrubber for Blender-authored motion graphics packs.

@onready var _player: MotionGraphicsPlayer = %MotionGraphicsPlayer
@onready var _list: ItemList = %PackList
@onready var _status: Label = %StatusLabel
@onready var _time: Label = %TimeLabel
@onready var _slider: HSlider = %ScrubSlider
@onready var _marker_log: ItemList = %MarkerLog

const MG_ROOT := "res://assets/motion_graphics"


func _ready() -> void:
	_refresh_packs()
	_player.time_changed.connect(_on_time_changed)
	_player.marker_reached.connect(_on_marker_reached)
	_player.playback_finished.connect(func() -> void: _status.text = "Finished")


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("af_back"):
		get_tree().change_scene_to_file("res://scenes/main.tscn")
	elif event.is_action_pressed("af_pause"):
		_player.toggle()


func _refresh_packs() -> void:
	_list.clear()
	var dir := DirAccess.open(MG_ROOT)
	if dir == null:
		_status.text = "Add packs under assets/motion_graphics/<Name>/*.glb"
		return
	dir.list_dir_begin()
	var entry := dir.get_next()
	while entry != "":
		if dir.current_is_dir() and not entry.begins_with("."):
			var folder := "%s/%s" % [MG_ROOT, entry]
			var glb := _find_glb(folder)
			if glb != "":
				var idx := _list.add_item(entry.replace("_", " "))
				_list.set_item_metadata(idx, {"glb": glb, "sidecar": GltfMeta.find_sidecar_for_glb(glb)})
		entry = dir.get_next()
	dir.list_dir_end()
	if _list.item_count == 0:
		_status.text = "No motion graphics packs found"
	else:
		_list.select(0)
		_load_selected(0)


func _on_pack_list_item_selected(index: int) -> void:
	_load_selected(index)


func _on_play_pressed() -> void:
	_player.play()
	_status.text = "Playing"


func _on_pause_pressed() -> void:
	_player.pause()
	_status.text = "Paused"


func _on_scrub_slider_value_changed(value: float) -> void:
	_player.seek(value)


func _on_time_changed(seconds: float) -> void:
	_time.text = "%.2fs / %.2fs" % [seconds, _player.duration]
	_slider.set_value_no_signal(seconds)


func _on_marker_reached(marker_name: String) -> void:
	_marker_log.add_item(marker_name)
	_status.text = "Marker: %s" % marker_name


func _load_selected(index: int) -> void:
	var pack: Dictionary = _list.get_item_metadata(index)
	var err := _player.load_scene(str(pack["glb"]), str(pack.get("sidecar", "")))
	if err != OK:
		_status.text = "Failed to load pack"
		return
	_slider.max_value = _player.duration
	_slider.value = 0.0
	_marker_log.clear()
	_status.text = "Loaded · layers: %s" % ", ".join(_player.layers)
	_player.play()


func _find_glb(folder: String) -> String:
	var dir := DirAccess.open(folder)
	if dir == null:
		return ""
	dir.list_dir_begin()
	var entry := dir.get_next()
	var found := ""
	while entry != "":
		if not dir.current_is_dir() and entry.to_lower().ends_with(".glb"):
			found = "%s/%s" % [folder, entry]
			break
		entry = dir.get_next()
	dir.list_dir_end()
	return found
