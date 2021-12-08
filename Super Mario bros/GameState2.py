from pico2d import *
import GameState3
import TitleState
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
	global mario, ground, cloud, pipe, background, bgm, pause, pipe_sound, kill_sound
	pause = False
	GameWorld.game_init(["bg", "platform", "block", "itembox", "coin", "coin2", "goomba", "mario", "mushroom", "pipe"])
	GameSprite.load()
	mario = Mario()
	GameWorld.add(7, mario, GameFramework.game_level)

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
	kill_sound = load_wav('resource/kill.wav')
	kill_sound.set_volume(200)
	bgm.set_volume(200)
	bgm.repeat_play()
def update():
	global pause
	if pause == False:
		GameWorld.update()
		if mario.dead == False:
			check_and_handle_collision()
		if mario.clear:
			if mario.x > 6760:
				GameWorld.clear()
				GameFramework.change(GameState3)
def draw():
	GameWorld.draw()
	mario.draw_ui()
def handle_event(event):
	global running, pause

	if (event.type == SDL_QUIT):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
		bgm.stop()
		GameFramework.change_level(1)
		GameWorld.clear()
		GameFramework.change(TitleState)

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
	global mario, bgm
	(lh, foot, rh, head) = mario.get_bb()

	# 굼바 충돌
	for goomba in GameWorld.objects_at(GameWorld.layer.goomba):
		if goomba.is_collide == False:
			if (GameObject.collides_box(mario, goomba)):
				(left, bottom, right, top) = goomba.get_bb()
				if foot >= top - 20:
					GameFramework.Score += 1000
					kill_sound.play()
					goomba.is_collide = True
				else:
					mario.life -= 1
					if mario.life == 0:
						mario.y_default = 100
						mario.y = 100
					if mario.life < 0:
						mario.falling_speed = Mario.JUMP
						bgm.stop()
						mario.life = 0
						mario.dead = True
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

	for coin2 in GameWorld.objects_at(GameWorld.layer.coin2):
		if (GameObject.collides_box(mario, coin2)):
			coin2.coin_sound.play()
			GameFramework.Total_coin += 1
			GameFramework.Score += 1000
			coin2.collide = True

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
	# pipe
	for pipe in GameWorld.objects_at(GameWorld.layer.pipe):
		if (GameObject.collides_box(mario, pipe)):
			bgm.stop()
			mario.clear = True

def exit():
	pass

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()