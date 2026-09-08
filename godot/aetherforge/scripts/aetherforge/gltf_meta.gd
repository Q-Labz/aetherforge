class_name GltfMeta
extends RefCounted
## Parses AetherForge extras from glTF custom data / sidecar JSON.

const AF_KEY := "aetherforge"


static func from_dictionary(data: Dictionary) -> Dictionary:
	if data.has(AF_KEY) and typeof(data[AF_KEY]) == TYPE_DICTIONARY:
		return data[AF_KEY]
	return data


static func from_sidecar(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return {}
	return from_dictionary(parsed)


static func find_sidecar_for_glb(glb_path: String) -> String:
	var base := glb_path.get_basename()
	return "%s.aetherforge.json" % base


static func kind(meta: Dictionary) -> String:
	return str(meta.get("kind", "prop"))


static func clip_names(meta: Dictionary) -> PackedStringArray:
	var out: PackedStringArray = []
	var clips: Variant = meta.get("clips", [])
	if typeof(clips) != TYPE_ARRAY:
		return out
	for item in clips:
		if typeof(item) == TYPE_DICTIONARY and item.has("name"):
			out.append(str(item["name"]))
		elif typeof(item) == TYPE_STRING:
			out.append(str(item))
	return out


static func motion_graphics(meta: Dictionary) -> Dictionary:
	var mg: Variant = meta.get("motion_graphics", {})
	return mg if typeof(mg) == TYPE_DICTIONARY else {}
