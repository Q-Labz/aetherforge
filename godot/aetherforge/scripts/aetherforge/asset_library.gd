extends Node
## Scans res://assets/characters for packed character glTF folders.

signal library_changed

const CHARACTERS_ROOT := "res://assets/characters"


func _ready() -> void:
	refresh()


func refresh() -> void:
	library_changed.emit()


func list_characters() -> Array[Dictionary]:
	var results: Array[Dictionary] = []
	var dir := DirAccess.open(CHARACTERS_ROOT)
	if dir == null:
		return results

	dir.list_dir_begin()
	var entry := dir.get_next()
	while entry != "":
		if dir.current_is_dir() and not entry.begins_with("."):
			var folder := "%s/%s" % [CHARACTERS_ROOT, entry]
			var glb := _find_glb(folder)
			if glb != "":
				results.append({
					"id": entry,
					"name": entry.replace("_", " "),
					"glb": glb,
					"sidecar": GltfMeta.find_sidecar_for_glb(glb),
				})
		entry = dir.get_next()
	dir.list_dir_end()
	results.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return str(a["name"]) < str(b["name"]))
	return results


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
