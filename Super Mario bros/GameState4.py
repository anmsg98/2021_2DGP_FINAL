from pico2d import *
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
time = 0

def enter():
    GameFramework.change_level(4)
    global mario, ground, cloud, pipe, background, bgm, pause
    pause = False
    GameWorld.game_init(["bg", "mario", "peach", "platform"])
    GameSprite.load()
    mario = Mario()
    GameWorld.add(1, mario, GameFramework.game_level)

    background = Background(GameFramework.game_level)
    GameWorld.add(0, background, GameFramework.game_level)

    background.set_center_object(mario)
    mario.set_background(background)

    with open("JSON/Stage4.json") as file:
        data = json.load(file)

    for info in data:
        obj = GameSprite.createObject(info, mario)
        GameWorld.add(info["layer_index"], obj, GameFramework.game_level)
        obj.set_background(background)
    GameWorld.curr_obj = GameWorld.stage4_obj
    bgm = load_music('resource/peach.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()
    mario.clear = True
def update():
    print(int(mario.x))
    global pause, time
    if pause == False:
        time += GameFramework.delta_time
        GameWorld.update()
        check_and_handle_collision()
    else:
        pass
def draw():
    GameWorld.draw()
    mario.draw_ui()
    mario.draw_credit(time)

def handle_event(event):
    global running, pause

    if (event.type == SDL_QUIT):
        GameFramework.quit()
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        GameFramework.change_level(1)
        bgm.stop()
        GameWorld.remove(mario)
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
    global mario
    (lh, foot, rh, head) = mario.get_bb()


def exit():
    pass

def pause():
    pass

def resume():
    pass

if (__name__ == "__main__"):
    GameFramework.run_main()