from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode
from grass import Grass


def init():
    global image, bgm
    image = load_image('.\\Resources\\UI\\main\\GameOver.png')
    bgm = load_music('.\\Resources\\bgm\\gameover.mp3')
    bgm.set_volume(32)
    bgm.play()

def finish():
    global image
    del image

def update():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def draw():
    clear_canvas()
    image.clip_composite_draw(0, 0, 1920, 1080, 0, '', 534, 300, 1067, 600)
    update_canvas()