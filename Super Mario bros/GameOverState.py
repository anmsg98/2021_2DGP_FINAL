from pico2d import *
import GameFramework
import GameWorld
import TitleState
count = 0
def enter():
    global background, font, elapsed, mario, bgm
    background = load_image("resource/gameover.png")
    bgm = load_wav("resource/gameover.wav")
    bgm.set_volume(100)
    GameFramework.Player_hp -= 1
    elapsed = 0

def update():
    global count
    if count == 0:
        bgm.play()
        count += 1
    pass

def draw():
    background.draw(400, 300)


def handle_event(event):
    global running, count

    if (event.type == SDL_QUIT):
        GameFramework.quit()
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        count = 0
        GameFramework.change(TitleState)

def exit():
    global background
    del background

def pause():
    pass

def resume():
    pass

if (__name__ == "__main__"):
    GameFramework.run_main()