from pico2d import *
from Mario import *
import GameFramework
import GameWorld
import GameSprite
import json

def enter():
	global mario, ground, cloud, pipe, background
	mario = Mario()
	GameWorld.add(3, mario)


	with open("JSON/Stage.json") as file:
		data = json.load(file)

	for info in data:
		object = GameSprite.Sprite(info["name"], info["x"], info["y"], info["w"], info["h"])
		GameWorld.add(info["layer_index"], object)

def update():
	GameWorld.update()

def draw():
	GameWorld.draw()

def handle_event(event):
	global running

	if (event.type == SDL_QUIT):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
		GameFramework.pop()

	mario.handle_event(event)

def exit():
	pass

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()