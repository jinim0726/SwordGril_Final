import random
import math
import game_framework
import game_world

from pico2d import *

from state_machine import start_event, time_out, dead, find_attack, StateMachine, find_run, miss, hurt

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed`
TIME_PER_ACTION = 1
ACTION_PER_TIME = 0.8 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']
class Idle:
    @staticmethod
    def enter(shaman, e):
        if start_event(e):
            shaman.face_dir = -1

        shaman.frame = 0
        shaman.wait_time = get_time()

    @staticmethod
    def exit(shaman, e):
        pass

    @staticmethod
    def do(shaman):
        shaman.frame = (shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % shaman.frame_rates['Idle']

    @staticmethod
    def draw(shaman):
        if shaman.face_dir == 1:
            shaman.image[0].clip_draw(int(shaman.frame) * 96, 0, 96, 96, shaman.x, shaman.y)
        else:
            shaman.image[0].clip_composite_draw(int(shaman.frame) * 96, 0, 96, 96, 0, 'h', shaman.x, shaman.y, 96, 96)

class Run:
    @staticmethod
    def enter(shaman, e):
        pass

    @staticmethod
    def exit(shaman, e):
        #if space_down(e): Shaman.fire_ball()
        pass

    @staticmethod
    def do(shaman):
        shaman.frame = (shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % shaman.frame_rates['Run']
        shaman.x += shaman.face_dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(shaman):
        if shaman.face_dir == 1:
            shaman.image[1].clip_draw(int(shaman.frame) * 96, 0, 96, 96, shaman.x, shaman.y)
        else:
            shaman.image[1].clip_composite_draw(int(shaman.frame) * 96, 0, 96, 96, 0, 'h', shaman.x, shaman.y, 96, 96)

class Hurt:
    @staticmethod
    def enter(shaman, e):
        print("Entered Hurt state")
        shaman.frame = 0
        shaman.current_frame = 0
        shaman.combo = 0
        pass

    @staticmethod
    def exit(shaman, e):
        print("Exited Hurt state")
        pass

    @staticmethod
    def do(shaman):
        shaman.frame = (shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % shaman.frame_rates['Hurt']
        shaman.current_frame = shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        if shaman.current_frame >= shaman.frame_rates['Hurt'] * 2:
            shaman.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(shaman):
        print("시바 왜 안그려 이걸로")
        if shaman.face_dir == 1:
            shaman.image[2].clip_draw(int(shaman.frame) * 96, 0, 96, 96, shaman.x, shaman.y)
        else:
            shaman.image[2].clip_composite_draw(int(shaman.frame) * 96, 0, 96, 96, 0, 'h', shaman.x, shaman.y, 96, 96)
        pass

class Magic_1:
    @staticmethod
    def enter(shaman, e):
        shaman.frame = 0
        shaman.current_frame = 0
        shaman.combo += 1
        shaman.attack_processed = False  # 공격 처리 완료 상태로 변경
        pass

    @staticmethod
    def exit(shaman, e):
        #if space_down(e): Shaman.fire_ball()
        pass

    @staticmethod
    def do(shaman):
        shaman.frame = (shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % shaman.frame_rates['Magic_1']
        shaman.current_frame = shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 8  # 공격 처리를 원하는 프레임
        if not shaman.attack_processed and int(shaman.current_frame) == attack_frame:
            shaman.attack = True
            shaman.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            shaman.attack = False

        if shaman.current_frame >= shaman.frame_rates['Magic_1']:
            shaman.y = 73
            shaman.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(shaman):
        if shaman.face_dir == 1:
            shaman.image[6].clip_draw(int(shaman.frame) * 96, 0, 96, 96, shaman.x, shaman.y)
        else:
            shaman.image[6].clip_composite_draw(int(shaman.frame) * 96, 0, 96, 96, 0, 'h', shaman.x, shaman.y, 96, 96)
        pass

class Magic_2:
    @staticmethod
    def enter(shaman, e):
        shaman.frame = 0
        shaman.current_frame = 0
        shaman.attack_processed = False  # 공격 처리 완료 상태로 변경
        pass

    @staticmethod
    def exit(shaman, e):
        #if space_down(e): Shaman.fire_ball()
        pass

    @staticmethod
    def do(shaman):
        shaman.frame = (shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % shaman.frame_rates['Magic_2']
        shaman.current_frame = shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 6  # 공격 처리를 원하는 프레임
        if not shaman.attack_processed and int(shaman.current_frame) == attack_frame:
            shaman.attack = True
            shaman.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            shaman.attack = False

        if shaman.current_frame >= shaman.frame_rates['Magic_2']:
            shaman.y = 73
            shaman.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(shaman):
        if shaman.face_dir == 1:
            shaman.image[6].clip_draw(int(shaman.frame) * 96, 0, 96, 96, shaman.x, shaman.y)
        else:
            shaman.image[6].clip_composite_draw(int(shaman.frame) * 96, 0, 96, 96, 0, 'h', shaman.x, shaman.y, 96, 96)
        pass

class Dead:
    @staticmethod
    def enter(shaman, e):
        shaman.frame = 0
        shaman.current_frame = 0
        pass

    @staticmethod
    def exit(shaman, e):
        #if space_down(e): Shaman.fire_ball()
        pass

    @staticmethod
    def do(shaman):
        if int(shaman.current_frame) < int(shaman.frame_rates['Dead']):
            shaman.frame = (shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                            shaman.frame_rates['Dead']
            shaman.current_frame = shaman.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        pass

    @staticmethod
    def draw(shaman):
        if shaman.face_dir == 1:
            shaman.image[7].clip_draw(int(shaman.frame) * 96, 0, 96, 96, shaman.x, shaman.y)
        else:
            shaman.image[7].clip_composite_draw(int(shaman.frame) * 96, 0, 96, 96, 0, 'h', shaman.x, shaman.y, 96, 96)
        pass

class Shaman:
    image = None

    def __init__(self):
        self.state_machine = StateMachine(self)
        self.frame = 0
        self.x, self.y = random.randint(1600-800, 1600), 73
        self.font = load_font('ENCR10B.TTF', 16)
        self.face_dir = -1
        self.hp = 150
        self.damage = 50
        self.exp = 10
        self.attack_x, self.attack_y = self.x, self.y
        self.attack = False
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle :      {time_out: Run, dead: Dead, hurt: Hurt},

                Run :       {find_attack: Magic_1, dead: Dead, hurt: Hurt},

                Hurt :      {time_out: Run, dead: Dead, hurt: Hurt},

                Magic_1 :   {time_out: Magic_2, miss: Run, dead: Dead, hurt: Hurt},

                Magic_2 :   {time_out: Magic_1, miss: Run, dead: Dead, hurt: Hurt},

                Dead :      {}
            }
        )
        self.frame_rates = {
            'Idle': 5,
            'Run': 6,
            'Hurt': 2,
            'Magic_1' : 8,
            'Magic_2' : 6,
            'Dead': 5
        }
        if Shaman.image is None:
            Shaman.image = [
                load_image('.\\Resources\\monster\\Orc_Shaman\\Idle.png'),
                load_image('.\\Resources\\monster\\Orc_Shaman\\Run.png'),
                load_image('.\\Resources\\monster\\Orc_Shaman\\Hurt.png'),
                load_image('.\\Resources\\monster\\Orc_Shaman\\Magic_1.png'),
                load_image('.\\Resources\\monster\\Orc_Shaman\\Magic_2.png'),
                load_image('.\\Resources\\monster\\Orc_Shaman\\Dead.png')
            ]

    def update(self):
        self.state_machine.update()
        #self.damage = 50 + (self.combo * 10)
        if self.hp <= 0:
            self.state_machine.add_event(('DEAD', 0))
        pass

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # 충돌 영역 그리기
        draw_rectangle(*self.get_bb('boy:shaman_find'))
        draw_rectangle(*self.get_bb('boy:shaman_attack'))
        draw_rectangle(*self.get_bb(''))
        self.font.draw(self.x, self.y + 50, f'combo : {self.combo:02d}', (255, 255, 0))
        self.font.draw(self.x, self.y + 70, f'hp : {self.hp:02d}', (255, 255, 0))

    def get_bb(self, group):
        if group == 'boy:shaman_dic':
                return self.x - 2000, self.y - 1000, self.x, self.y + 1000
        if group == 'boy:shaman_attack':
            if self.face_dir == 1:
                if self.state_machine.cur_state == Magic_1:
                    return self.x + 50, self.y - 50, self.x + 10, self.y + 50
                elif self.state_machine.cur_state == Magic_2:
                    return self.x + 50, self.y - 50, self.x + 10, self.y + 50
                else:
                    return self.x - 50, self.y - 50, self.x - 10, self.y + 50
            elif self.face_dir == -1:
                if self.state_machine.cur_state == Magic_1:
                    return self.x + 50, self.y - 50, self.x + 10, self.y + 50
                elif self.state_machine.cur_state == Magic_2:
                    return self.x + 50, self.y - 50, self.x + 10, self.y + 50
                else:
                    return self.x - 50, self.y - 50, self.x - 10, self.y + 50
        if group == 'boy:shaman_find':
                return self.x - 150, self.y - 50, self.x + 150, self.y + 50
        else:
            return self.x - 28, self.y - 48, self.x + 28, self.y + 18

    def handle_collision(self, group, other, on):
        if self.state_machine.cur_state != Dead:
            if group == 'boy_attack:shaman' and on and other.attack:
                print(F'{group} collide {on}')
                self.state_machine.add_event(('HURT', 0))
                self.hp -= other.damage
                self.x += other.face_dir * 10
            if group == 'boy:shaman_find':
                if on:
                    if self.state_machine.cur_state == Run:
                        #print(F'{group} collide {on}')
                        self.state_machine.add_event(('FIND_ATTACK', 0))
                    elif self.state_machine.cur_state in (Magic_1, Magic_2):
                        # print(F'{group} collide {on}')
                        if self.frame < 4:
                            self.attack_x = other.x
                            self.attack_y = other.y
                else:
                    if self.state_machine.cur_state in (Magic_1, Magic_2):
                        #print(F'{group} collide {on}')
                        self.state_machine.add_event(('MISS', 0))
            if group == 'boy:shaman_dic':
                #print(F'{group} collide {on}')
                if on:
                    if self.face_dir == 1:
                        self.face_dir = -1
                else:
                    if self.face_dir == -1:
                        self.face_dir = 1
        pass