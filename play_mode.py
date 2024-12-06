import random

from pico2d import *
import game_framework

import game_world
from Warrior import Warrior
from boy import Boy
from Berserk import Berserk
from Warrior import Warrior
from grass import Grass


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
    global grass
    global boy
    global berserks
    global warriors

    grass = Grass()
    game_world.add_object(grass, 0)
    grass.bgm.repeat_play()

    boy = Boy()
    game_world.add_object(boy, 1)

    berserks = [Berserk() for _ in range(1)]
    game_world.add_objects(berserks, 1)

    warriors = [Warrior() for _ in range(1)]
    game_world.add_objects(warriors, 1)

    add_collision_pairs()

def add_collision_pairs():
    global boy, berserks, warriors

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

    # 타이머 업데이트
    grass.spawn_time += game_framework.frame_time

    # 특정 시간이 지나면 몬스터 생성
    if grass.spawn_time >= grass.MONSTER_SPAWN_INTERVAL:
        spawn_monsters(grass.BERSERK_COUNT, 'Berserk')  # 생성할 몬스터 수
        spawn_monsters(grass.WARRIOR_COUNT, 'Warrior')

        grass.spawn_time = 0  # 타이머 초기화

def spawn_monsters(count, type):
    global berserks, warriors
    if type == 'Berserk':
        new_berserks = [Berserk() for _ in range(count)]
        game_world.add_objects(new_berserks, 1)
        berserks.extend(new_berserks)

        for berserk in new_berserks:
            game_world.add_collision_pair('boy:berserk_attack', None, berserk)
            game_world.add_collision_pair('boy_attack:berserk', None, berserk)
            game_world.add_collision_pair('boy:berserk_find', None, berserk)
            game_world.add_collision_pair('boy:berserk_dic', None, berserk)

        count += 1

    if type == 'Warrior':
        new_warriors = [Warrior() for _ in range(count)]
        game_world.add_objects(new_warriors, 1)
        warriors.extend(new_warriors)

        for warrior in new_warriors:
            game_world.add_collision_pair('boy:warrior_attack', None, warrior)
            game_world.add_collision_pair('boy_attack:warrior', None, warrior)
            game_world.add_collision_pair('boy:warrior_find', None, warrior)
            game_world.add_collision_pair('boy:warrior_dic', None, warrior)

        count += 1

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
