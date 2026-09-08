extends Node3D
## Interactive stage that lists packed characters and plays their clips.

@onready var _actor: CharacterActor = %CharacterActor
@onready var _list: ItemList = %CharacterList
@onready var _clips: ItemList = %ClipList
@onready var _status: Label = %StatusLabel
@onready var _hint: Label = %HintLabel


func _ready() -> void:
	_hint.text = "1-9 clips · Space pause · R reset · Esc menu"
	_refresh_library()
	AssetLibrary.library_changed.connect(_refresh_library)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("af_back"):
		get_tree().change_scene_to_file("res://scenes/main.tscn")
		return
	if event.is_action_pressed("af_pause"):
		_actor.toggle_pause()
		return
	if event.is_action_pressed("af_reset"):
		_actor.reset_to_first()
		return
	if event is InputEventKey and event.pressed and not event.echo:
		var key := event.keycode
		if key >= KEY_1 and key <= KEY_9:
			_actor.play_clip_index(key - KEY_1)


func _refresh_library() -> void:
	_list.clear()
	for character in AssetLibrary.list_characters():
		var idx := _list.add_item(str(character["name"]))
		_list.set_item_metadata(idx, character)
	if _list.item_count == 0:
		_status.text = "No characters yet — export a .glb into assets/characters/<Name>/"
	else:
		_status.text = "%d character pack(s) ready" % _list.item_count
		_list.select(0)
		_load_selected()


func _on_character_list_item_selected(index: int) -> void:
	_load_selected(index)


func _on_clip_list_item_selected(index: int) -> void:
	_actor.play_clip_index(index)


func _load_selected(index: int = -1) -> void:
	if _list.item_count == 0:
		return
	if index < 0:
		var selected := _list.get_selected_items()
		if selected.is_empty():
			return
		index = selected[0]
	var character: Dictionary = _list.get_item_metadata(index)
	var err := _actor.load_character(str(character["glb"]), str(character.get("sidecar", "")))
	if err != OK:
		_status.text = "Failed to load %s" % character["name"]
		return
	_status.text = "Loaded %s (%s)" % [character["name"], GltfMeta.kind(_actor.meta)]
	_clips.clear()
	for clip_name in _actor.get_clip_names():
		_clips.add_item(clip_name)
