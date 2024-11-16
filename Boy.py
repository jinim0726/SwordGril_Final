# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font, \
    draw_rectangle, KMOD_SHIFT
import os

from sdl2 import SDL_GetModState

import game_world
import game_framework
from state_machine import (start_event, a_up, a_down, w_up, w_down, s_up, s_down,
                           d_up, d_down, j_up, j_down, hit, dead, StateMachine, time_out)

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

ACTION_PER_ATTACK = 1.0 / TIME_PER_ACTION


class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
        elif a_down(e):
            boy.face_dir = 1
        elif d_down(e):
            boy.face_dir = -1

        boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 6
        # boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 2:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[0].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[0].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)

class Run:
    @staticmethod
    def enter(boy, e):
        if d_down(e): # 오른쪽으로 RUN
            boy.face_dir = 1
        elif a_down(e): # 왼쪽으로 RUN
            boy.face_dir = -1

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 8

        if SDL_GetModState() & KMOD_SHIFT:
            boy.x += boy.face_dir * RUN_SPEED_PPS * 1.5 * game_framework.frame_time
        else:
            boy.x += boy.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(boy):
        if SDL_GetModState() & KMOD_SHIFT:
            if boy.face_dir == 1:
                boy.image[2].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x + 20, boy.y)
            else:
                boy.image[2].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x - 20, boy.y, 128, 128)
        else:
            if boy.face_dir == 1:
                boy.image[1].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
            else:
                boy.image[1].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Jump:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        if d_down(e) or a_up(e): # 오른쪽으로 Jump
            boy.face_dir = 1
        elif a_down(e) or d_up(e): # 왼쪽으로 Jump
            boy.face_dir = -1
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 12

        if(boy.frame < 6):
            boy.x += boy.face_dir * RUN_SPEED_PPS / 2 * game_framework.frame_time
            boy.y += RUN_SPEED_PPS * game_framework.frame_time
        else:
            boy.x += boy.face_dir * RUN_SPEED_PPS / 2 * game_framework.frame_time
            boy.y -= RUN_SPEED_PPS * game_framework.frame_time

        if(boy.frame > 11.9):
            boy.y = 90
            boy.state_machine.add_event(('TIME_OUT', 0))
            pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[3].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[3].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Hurt:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        boy.hp -= 10
        boy.combo = 0
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 2;
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[4].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[4].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Shield:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        if(int(boy.frame) != 1):
            boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 2;
        else:
            boy.frame = 1
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[5].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[5].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Attack_1:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        boy.combo += 1
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_ATTACK * game_framework.frame_time) % 6;

        if(boy.frame > 5.5):
            boy.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[6].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[6].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Attack_2:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        boy.combo += 1
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_ATTACK * game_framework.frame_time) % 4;

        if(boy.frame > 3.9):
            boy.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[7].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[7].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Attack_3:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        boy.combo += 1
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_ATTACK * game_framework.frame_time) % 3;

        if(boy.frame > 2.9):
            boy.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[8].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[8].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Dead:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % 3;
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[9].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[9].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class Boy:
    image = None

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.combo = 0
        self.hp = 100
        self.damage = 50 + (self.combo * 10)
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.attack = False
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle :      {a_down: Run, d_down: Run, s_down: Shield,
                                w_down: Jump, j_down: Attack_1, dead: Dead, hit: Hurt},

                Run :       {a_down: Idle, a_up: Idle, d_down: Idle, d_up: Idle, j_down: Attack_1,
                                w_down: Jump, s_down: Shield, dead: Dead, hit: Hurt},

                Jump :      {time_out: Idle, dead: Dead},

                Hurt :      {time_out: Idle, dead: Dead},

                Shield :    {s_up: Idle, dead: Dead},

                Attack_1 :  {time_out: Attack_2, j_up: Idle, dead: Dead, hit: Hurt},

                Attack_2 :  {time_out: Attack_3, j_up: Idle, dead: Dead, hit: Hurt},

                Attack_3 :  {time_out: Attack_1, j_up: Idle, dead: Dead, hit: Hurt},
            }
        )
        self.frame_rates = {
            'Idle': 6,
            'Walk': 4,
            'Run': 8,
            'Jump': 12,
            'Hurt': 2,
            'Shield': 2,
            'Attack_1': 6,
            'Attack_2': 4,
            'Attack_3': 3,
            'Dead': 3
        }
        if Boy.image == None:
            print("Current working directory:", os.getcwd())
            Boy.image = [
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Idle.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Walk.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Run.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Jump.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Hurt.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Shield.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Attack_1.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Attack_2.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Attack_3.png'),
            load_image('..\\SwordGirl_3\\Resources\\character\\Samurai\\Dead.png')
            ]

    def update(self):
        self.state_machine.update()
        self.damage = 50 + (self.combo * 10)

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # 충돌 영역 그리기
        draw_rectangle(*self.get_bb('boy_attack:berserk'))
        draw_rectangle(*self.get_bb('boy:berserk_attack'))
        draw_rectangle(*self.get_bb(''))
        self.font.draw(self.x, self.y + 50, f'{self.combo:02d}', (255, 255, 0))
        self.font.draw(self.x, self.y + 70, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self, group):
        if group == 'boy_attack:berserk':
            if self.face_dir == 1:
                return self.x + 20, self.y - 40, self.x + 65, self.y
            else:
                return self.x - 65, self.y - 40, self.x - 20, self.y
        else:
            return self.x - 20, self.y - 70, self.x + 20, self.y + 20
        pass

    def handle_collision(self, group, other, on):
        # fill here
        if group == 'boy:berserk_attack' and on:
            if on:
                print(F'{group} collide {on}')
                if self.state_machine.cur_state == Shield:
                    self.combo += 1
        pass