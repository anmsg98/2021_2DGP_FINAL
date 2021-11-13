from pico2d import *
from background import FixedBackground as Background
from Mario import *
import GameFramework
import GameObject
import GameWorld
import GameSprite
import json


def enter():
	global mario, ground, cloud, pipe, background
	GameWorld.game_init(["bg", "platform", "itembox", "coin", "goomba", "mario"])
	GameSprite.load()
	mario = Mario()
	GameWorld.add(5, mario)

	background = Background()
	GameWorld.add(0, background)

	background.set_center_object(mario)
	mario.set_background(background)

	with open("JSON/Stage.json") as file:
		data = json.load(file)

	for info in data:
		obj = GameSprite.createObject(info)
		GameWorld.add(info["layer_index"], obj)
		obj.set_background(background)
	GameWorld.curr_obj = GameWorld.stage_obj
def update():
	GameWorld.update()
	check_and_handle_collision()
def draw():
	GameWorld.draw()

def handle_event(event):
	global running

	if (event.type == SDL_QUIT):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
		GameFramework.pop()

	mario.handle_event(event)


def check_and_handle_collision():
	global mario
	for goomba in GameWorld.objects_at(GameWorld.layer.goomba):
		if (GameObject.collides_box(mario, goomba)):
			goomba.is_collide = True



def exit():
	pass

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()