from pico2d import *
import GameFramework
import GameState

def enter():
	global background
	GameFramework.init()
	background = load_image("resource/Title.png")

def update():
	pass

def draw():
	background.draw(400, 300)

def handle_event(event):
	global running

	if (event.type == SDL_QUIT):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
		GameFramework.quit()
	elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
		GameFramework.push(GameState)

def exit():
	global background

def pause():
	pass

def resume():
	pass

if (__name__ == "__main__"):
	GameFramework.run_main()