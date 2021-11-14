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
	GameWorld.game_init(["bg", "platform", "block", "itembox", "coin", "goomba", "mario"])
	GameSprite.load()
	mario = Mario()
	GameWorld.add(6, mario)

	background = Background()
	GameWorld.add(0, background)

	background.set_center_object(mario)
	mario.set_background(background)

	with open("JSON/Stage.json") as file:
		data = json.load(file)

	for info in data:
		obj = GameSprite.createObject(info, mario)
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
	(lh, foot, rh, head) = mario.get_bb()

	# 굼바 충돌
	for goomba in GameWorld.objects_at(GameWorld.layer.goomba):
		if (GameObject.collides_box(mario, goomba)):
			goomba.is_collide = True
		# 굼바 & 플랫폼 충돌

	# 일반 박스 충돌
	for block in GameWorld.objects_at(GameWorld.layer.block):
		(left, bottom, right, top) = block.get_bb()
		if (GameObject.collides_box(mario, block)):
			if head >= bottom and foot < bottom:
				block.is_collide = True
	# 아이템 박스 충돌
	for itembox in GameWorld.objects_at(GameWorld.layer.itembox):
		(left, bottom, right, top) = itembox.get_bb()
		if (GameObject.collides_box(mario, itembox)):
			if head >= bottom and foot < bottom:
				itembox.is_collide = True
	for goomba in GameWorld.objects_at(GameWorld.layer.goomba):
		for platform in GameWorld.objects_at(GameWorld.layer.platform):
			(left, bottom, right, top) = platform.get_bb()
			if (GameObject.collides_box(goomba, platform)):
				if goomba.dir == -1:
					goomba.pos[0] += 1
					goomba.dir = 1
				else:
					goomba.pos[0] -= 1
					goomba.dir = -1

def exit():
	pass

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()