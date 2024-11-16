import random
import math
import game_framework
import game_world

from pico2d import *

from state_machine import start_event, time_out, dead, hit, find_attack, StateMachine, find_run, miss

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.8 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']
class Idle:
    @staticmethod
    def enter(Warrior, e):
        if start_event(e):
            Warrior.face_dir = -1

        Warrior.frame = 0
        Warrior.wait_time = get_time()

    @staticmethod
    def exit(Warrior, e):
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME
                         * game_framework.frame_time) % Warrior.frame_rates['Idle']

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[0].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[0].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)

class Run:
    @staticmethod
    def enter(Warrior, e):
        pass

    @staticmethod
    def exit(Warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['Run']

        if SDL_GetModState() & KMOD_SHIFT:
            Warrior.x += Warrior.face_dir * RUN_SPEED_PPS * 1.5 * game_framework.frame_time
        else:
            Warrior.x += Warrior.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[1].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[1].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)

class Hurt:
    @staticmethod
    def enter(Warrior, e):
        Warrior.frame = 0
        Warrior.combo = 0

        if(Warrior.hp <= 0):
            Warrior.state_machine.add_event(('DEAD', 0))
        pass

    @staticmethod
    def exit(Warrior, e):
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['Hurt']
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[2].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[2].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)
        pass

class Attack_1:
    @staticmethod
    def enter(Warrior, e):
        Warrior.frame = 0
        Warrior.combo += 1
        pass

    @staticmethod
    def exit(Warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['Attack_1']

        if(Warrior.frame > 3.9):
            Warrior.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[3].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[3].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)
        pass

class Attack_2:
    @staticmethod
    def enter(Warrior, e):
        Warrior.frame = 0
        Warrior.combo += 1
        pass

    @staticmethod
    def exit(Warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['Attack_2']

        if(Warrior.frame > 4.9):
            Warrior.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[4].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[4].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)
        pass

class Attack_3:
    @staticmethod
    def enter(Warrior, e):
        Warrior.frame = 0
        Warrior.combo += 1
        pass

    @staticmethod
    def exit(Warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['Attack_3']

        if(Warrior.frame > 1.9):
            Warrior.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[5].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[5].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)
        pass

class RunAttack:
    @staticmethod
    def enter(Warrior, e):
        Warrior.frame = 0
        Warrior.combo += 1
        pass

    @staticmethod
    def exit(Warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['RunAttack']

        if(Warrior.frame < 2.5):
            Warrior.x += Warrior.face_dir * RUN_SPEED_PPS * 3 * game_framework.frame_time
            Warrior.y += RUN_SPEED_PPS * game_framework.frame_time
        else:
            Warrior.x += Warrior.face_dir * RUN_SPEED_PPS * 3 * game_framework.frame_time
            Warrior.y -= RUN_SPEED_PPS * game_framework.frame_time


        if(Warrior.frame > 4.9):
            Warrior.y = 73
            Warrior.state_machine.add_event(('TIME_OUT', 0))
            pass
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[6].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[6].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)
        pass

class Dead:
    @staticmethod
    def enter(Warrior, e):
        Warrior.frame = 0
        pass

    @staticmethod
    def exit(Warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(Warrior):
        Warrior.frame = (Warrior.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % Warrior.frame_rates['Dead']
        pass

    @staticmethod
    def draw(Warrior):
        if Warrior.face_dir == 1:
            Warrior.image[7].clip_draw(int(Warrior.frame) * 96, 0, 96, 96, Warrior.x, Warrior.y)
        else:
            Warrior.image[7].clip_composite_draw(int(Warrior.frame) * 96, 0, 96, 96, 0, 'h', Warrior.x, Warrior.y, 96, 96)
        pass

class Warrior:
    image = None

    def __init__(self):
        self.state_machine = StateMachine(self)
        self.frame = 0
        self.x, self.y = random.randint(1600-800, 1600), 73
        self.font = load_font('ENCR10B.TTF', 16)
        self.face_dir = -1
        self.hp = 150
        self.damage = 30
        self.combo = 0
        self.exp = 10
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle :      {time_out: Run, dead: Dead, hit: Hurt},

                Run :       {find_attack: RunAttack, dead: Dead, hit: Hurt},

                Hurt :      {time_out: Run, dead: Dead, hit: Hurt},

                Attack_1 :  {time_out: Attack_2, miss: Run, dead: Dead, hit: Hurt},

                Attack_2 :  {time_out: Attack_3, miss: Run, dead: Dead, hit: Hurt},

                Attack_3 :  {time_out: Attack_1, miss: Run, dead: Dead, hit: Hurt},

                RunAttack : {time_out: Attack_1, miss: Run, dead: Dead, hit: Hurt}
            }
        )
        self.frame_rates = {
            'Idle': 5,
            'Run': 6,
            'Hurt': 2,
            'Attack_1': 4,
            'Attack_2': 4,
            'Attack_3': 3,
            'RunAttack' : 4,
            'Dead': 4
        }
        if Warrior.image == None:
            Warrior.image = [
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Idle.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Run.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Hurt.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Attack_1.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Attack_2.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Attack_3.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Run+Attack.png'),
                load_image('..\\SwordGirl_3\\Resources\\monster\\Orc_Warrior\\Dead.png')
            ]

    def update(self):
        self.state_machine.update()
        self.damage = 80 + (self.combo * 10)

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # 충돌 영역 그리기
        draw_rectangle(*self.get_bb('boy_attack:Warrior'))
        #draw_rectangle(*self.get_bb('boy:Warrior_find'))
        draw_rectangle(*self.get_bb('boy:Warrior_attack'))
        draw_rectangle(*self.get_bb(''))
        self.font.draw(self.x, self.y + 50, f'{self.combo:02d}', (255, 255, 0))
        self.font.draw(self.x, self.y + 70, f'{self.hp:02d}', (255, 255, 0))

    def get_bb(self, group):
        if group == 'boy:Warrior_dic':
            return self.x - 1000, self.y - 48, self.x, self.y + 18
        if group == 'boy_attack:Warrior':
            return self.x - 28, self.y - 48, self.x + 28, self.y + 18
        if group == 'boy:Warrior_attack':
            if self.state_machine.cur_state == Attack_1:
                return self.x - 50, self.y - 50, self.x - 10, self.y + 50
            elif self.state_machine.cur_state == Attack_2:
                return self.x - 50, self.y - 50, self.x - 10, self.y + 50
            elif self.state_machine.cur_state == Attack_3:
                return self.x - 50, self.y - 50, self.x - 10, self.y + 50
            elif self.state_machine.cur_state == RunAttack:
                return self.x - 50, self.y - 50, self.x - 10, self.y + 50
            else:
                return self.x - 50, self.y - 50, self.x - 10, self.y + 50
        if group == 'boy:Warrior_find':
            return self.x - 150, self.y - 50, self.x + 150, self.y + 50
        else:
            return self.x - 28, self.y - 48, self.x + 28, self.y + 18

    def handle_collision(self, group, other, on):
        if group == 'boy_attack:Warrior':
            if on:
                #print(F'{group} collide {on}')
                self.state_machine.add_event(('Hurt', 0))
                self.hp -= other.damage
        if group == 'boy:Warrior_find':
            if on:
                if self.state_machine.cur_state == Run:
                    #print(F'{group} collide {on}')
                    self.state_machine.add_event(('FIND_ATTACK', 0))
            else:
                if self.state_machine.cur_state in (Attack_1, Attack_2, Attack_3):
                    #print(F'{group} collide {on}')
                    self.state_machine.add_event(('MISS', 0))
        if group == 'boy:Warrior_attack':
            if on:
                pass
            else:
                pass
        if group == 'boy:Warrior_dic':
            print(F'{group} collide {on}')
            if on:
                if self.face_dir == 1:
                    self.face_dir = -1
            else:
                if self.face_dir == -1:
                    self.face_dir = 1
        pass