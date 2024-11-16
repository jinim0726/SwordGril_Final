import random

from pico2d import *
import game_framework

import game_world
from Warrior import Warrior
from boy import Boy
from Berserk import Berserk
from Warrior import Warrior
# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global berserks
    global warriors

    boy = Boy()
    game_world.add_object(boy, 1)

    berserks = [Berserk() for _ in range(1)]
    game_world.add_objects(berserks, 1)

    warriors = [Warrior() for _ in range(1)]
    game_world.add_objects(warriors, 1)

    game_world.add_collision_pair('boy:berserk_attack', boy, None)
    game_world.add_collision_pair('boy_attack:berserk', boy, None)
    game_world.add_collision_pair('boy:berserk_find', boy, None)
    game_world.add_collision_pair('boy:berserk_dic', boy, None)

    game_world.add_collision_pair('boy:warrior_attack', boy, None)
    game_world.add_collision_pair('boy_attack:warrior', boy, None)
    game_world.add_collision_pair('boy:warrior_find', boy, None)
    game_world.add_collision_pair('boy:warrior_dic', boy, None)

    for berserk in berserks:
        game_world.add_collision_pair('boy:berserk_attack', None, berserk)
        game_world.add_collision_pair('boy_attack:berserk', None, berserk)
        game_world.add_collision_pair('boy:berserk_find', None, berserk)
        game_world.add_collision_pair('boy:berserk_dic', None, berserk)

    for warrior in warriors:
        game_world.add_collision_pair('boy:warrior_attack', None, warrior)
        game_world.add_collision_pair('boy_attack:warrior', None, warrior)
        game_world.add_collision_pair('boy:warrior_find', None, warrior)
        game_world.add_collision_pair('boy:warrior_dic', None, warrior)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # fill here

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

