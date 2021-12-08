from pico2d import *
import GameFramework
import GameState, GameState2
import TitleState

def enter():
	global background, font, elapsed, mario
	background = load_image("resource/Dead.png")
	mario = load_image("resource/mario.png")
	font = load_font('resource/SuperMario3.ttf', 34)
	GameFramework.Player_hp -= 1
	elapsed = 0

def update():
	global elapsed

	elapsed += GameFramework.delta_time

	if (elapsed > 2.0):
		if GameFramework.game_level == 1:
			GameFramework.change(GameState)
		else:
			GameFramework.change(GameState2)

def draw():
	background.draw(400, 300)
	mario.clip_draw(420, 870, 30, 30, 290, 305, 40, 40)
	font.draw(250, 400, "WORLD 1-%d" % GameFramework.game_level, (255, 255, 255))
	font.draw(380, 300, "x  %d" % GameFramework.Player_hp, (255, 255, 255))


def handle_event(event):
	global running

	if (event.type == SDL_QUIT):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
		GameFramework.quit()

def exit():
	global background
	del background

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()