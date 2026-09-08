extends Control
## Boot menu for AetherForge demos.

@onready var _title: Label = %Title
@onready var _subtitle: Label = %Subtitle


func _ready() -> void:
	_title.text = "AetherForge"
	_subtitle.text = "Character Creator · Blender · Godot"


func _on_character_stage_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/character_stage.tscn")


func _on_motion_graphics_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/motion_graphics_demo.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
