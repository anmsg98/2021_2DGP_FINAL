from pico2d import *
from background import FixedBackground as Background
from Mario import *
import GameFramework
import GameObject
import GameWorld
import GameSprite
import json

pause = None
bgm = None


def enter():
	GameFramework.change_level(2)
	global mario, ground, cloud, pipe, background, bgm, pause
	pause = False
	GameWorld.game_init(["bg", "platform", "block", "itembox", "coin", "goomba", "mario", "mushroom", "flag"])
	GameSprite.load()
	mario = Mario()
	GameWorld.add(6, mario, GameFramework.game_level)

	background = Background(GameFramework.game_level)
	GameWorld.add(0, background, GameFramework.game_level)

	background.set_center_object(mario)
	mario.set_background(background)

	with open("JSON/Stage2.json") as file:
		data = json.load(file)

	for info in data:
		obj = GameSprite.createObject(info, mario)
		GameWorld.add(info["layer_index"], obj, GameFramework.game_level)
		obj.set_background(background)
	GameWorld.curr_obj = GameWorld.stage2_obj
	bgm = load_music('resource/bgm2.mp3')
	bgm.set_volume(64)
	bgm.repeat_play()

def update():
	global pause
	if pause == False:
		GameWorld.update()
		check_and_handle_collision()
def draw():
	GameWorld.draw()
	mario.draw_ui()
def handle_event(event):
	global running, pause

	if (event.type == SDL_QUIT):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
		GameFramework.pop()

	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
		if pause:
			bgm.play()
			pause = False
		else:
			bgm.stop()
			pause = True
	if pause == False:
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
	# 코인 충돌
	for coin in GameWorld.objects_at(GameWorld.layer.coin):
		if (GameObject.collides_box(mario, coin)):
			coin.coin_sound.play()
			GameFramework.Total_coin += 1
			GameFramework.Score += 1000
			coin.pos[1] += 40
			coin.collide = True

	# 버섯 충돌
	for mushroom in GameWorld.objects_at(GameWorld.layer.mushroom):
		if (GameObject.collides_box(mario, mushroom)):
			if mushroom.active:
				mario.increase_sound.play()
				mario.life = 1
				mario.y_default = 120
				GameWorld.remove(mushroom)
			else:
				mushroom.sound.play()
				GameFramework.Score += 300
				mushroom.collide = True
	# 깃발 충돌
	for flag in GameWorld.objects_at(GameWorld.layer.flag):
		if (GameObject.collides_box(mario, flag)):
			mario.clear = True

def exit():
	pass

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()