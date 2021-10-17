from pico2d import *
import GameFramework
import TitleState

def enter():
	global background, elapsed

	background = load_image("Image/KPU.png")
	elapsed = 0

def update():
	global elapsed

	elapsed += GameFramework.delta_time

	if (elapsed > 1.0):
		GameFramework.change(TitleState)

def draw():
	background.draw(400, 300)

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