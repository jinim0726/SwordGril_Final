import random
import math
import game_framework
import game_world

from pico2d import *

import play_mode
from state_machine import start_event, time_out, dead, find_attack, StateMachine, find_run, miss, hurt

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed`
TIME_PER_ACTION = 0.6
ACTION_PER_TIME = 0.8 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']
class Idle:
    @staticmethod
    def enter(warrior, e):
        if start_event(e):
            warrior.face_dir = -1

        warrior.frame = 0
        warrior.wait_time = get_time()

    @staticmethod
    def exit(warrior, e):
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['Idle']

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[0].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[0].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)

class Run:
    @staticmethod
    def enter(warrior, e):
        #warrior.zombie_run_bgm.play(1)
        pass

    @staticmethod
    def exit(warrior, e):
        #if space_down(e): Warrior.fire_ball()
        #warrior.zombie_run_bgm.stop()
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['Run']
        warrior.x += warrior.face_dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[1].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[1].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)

class Hurt:
    @staticmethod
    def enter(warrior, e):
        print("Entered Hurt state")
        warrior.frame = 0
        warrior.current_frame = 0
        warrior.y = 73
        warrior.zombie_hurt_bgm.play(1)
        pass

    @staticmethod
    def exit(warrior, e):
        print("Exited Hurt state")
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['Hurt']
        warrior.current_frame = warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        if warrior.current_frame >= warrior.frame_rates['Hurt']:
            warrior.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[2].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
            warrior.effect.clip_composite_draw(0, 0, 1280, 720, 0, '', warrior.x, warrior.y, 128, 128)
        else:
            warrior.image[2].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)
            warrior.effect.clip_composite_draw(0, 0, 1280, 720, 0, '', warrior.x, warrior.y, 128, 128)
        pass

class Attack_1:
    @staticmethod
    def enter(warrior, e):
        warrior.frame = 0
        warrior.current_frame = 0
        warrior.attack_processed = False  # 공격 처리 완료 상태로 변경
        warrior.zombie_attack_bgm.play(1)
        pass

    @staticmethod
    def exit(warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['Attack_1']
        warrior.current_frame = warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 3  # 공격 처리를 원하는 프레임
        if not warrior.attack_processed and int(warrior.current_frame) == attack_frame:
            warrior.attack = True
            warrior.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            warrior.attack = False

        if warrior.current_frame >= warrior.frame_rates['Attack_1']:
            warrior.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[3].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[3].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)
        pass

class Attack_2:
    @staticmethod
    def enter(warrior, e):
        warrior.frame = 0
        warrior.current_frame = 0
        warrior.attack_processed = False  # 공격 처리 완료 상태로 변경
        warrior.zombie_attack_bgm.play(1)
        pass

    @staticmethod
    def exit(warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['Attack_2']
        warrior.current_frame = warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 3  # 공격 처리를 원하는 프레임
        if not warrior.attack_processed and int(warrior.current_frame) == attack_frame:
            warrior.attack = True
            warrior.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            warrior.attack = False

        if warrior.current_frame >= warrior.frame_rates['Attack_2']:
            warrior.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[4].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[4].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)
        pass

class Attack_3:
    @staticmethod
    def enter(warrior, e):
        warrior.frame = 0
        warrior.current_frame = 0
        warrior.attack_processed = False  # 공격 처리 완료 상태로 변경
        warrior.zombie_attack_bgm.play(1)
        pass

    @staticmethod
    def exit(warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['Attack_3']
        warrior.current_frame = warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 2  # 공격 처리를 원하는 프레임
        if not warrior.attack_processed and int(warrior.current_frame) == attack_frame:
            warrior.attack = True
            warrior.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            warrior.attack = False

        if warrior.current_frame >= warrior.frame_rates['Attack_3']:
            warrior.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[5].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[5].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)
        pass

class RunAttack:
    @staticmethod
    def enter(warrior, e):
        warrior.frame = 0
        warrior.current_frame = 0
        warrior.attack_processed = False  # 공격 처리 완료 상태로 변경
        pass

    @staticmethod
    def exit(warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % warrior.frame_rates['RunAttack']
        warrior.current_frame = warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 4  # 공격 처리를 원하는 프레임
        if not warrior.attack_processed and int(warrior.current_frame) == attack_frame:
            warrior.attack = True
            warrior.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            warrior.attack = False

        if warrior.frame < (warrior.frame_rates['RunAttack'] / 2):
            warrior.x += warrior.face_dir * RUN_SPEED_PPS * 3 * game_framework.frame_time
            warrior.y += RUN_SPEED_PPS * game_framework.frame_time
        else:
            warrior.x += warrior.face_dir * RUN_SPEED_PPS * 3 * game_framework.frame_time
            warrior.y -= RUN_SPEED_PPS * game_framework.frame_time

        if warrior.current_frame >= warrior.frame_rates['RunAttack']:
            warrior.y = 73
            warrior.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[6].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[6].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)
        pass

class Dead:
    @staticmethod
    def enter(warrior, e):
        warrior.frame = 0
        warrior.current_frame = 0

        play_mode.Grass.score += warrior.score
        pass

    @staticmethod
    def exit(warrior, e):
        #if space_down(e): Warrior.fire_ball()
        pass

    @staticmethod
    def do(warrior):
        if int(warrior.current_frame) < int(warrior.frame_rates['Dead']):
            warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                            warrior.frame_rates['Dead']
            warrior.current_frame = warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        pass

    @staticmethod
    def draw(warrior):
        if warrior.face_dir == 1:
            warrior.image[7].clip_draw(int(warrior.frame) * 96, 0, 96, 96, warrior.x, warrior.y)
        else:
            warrior.image[7].clip_composite_draw(int(warrior.frame) * 96, 0, 96, 96, 0, 'h', warrior.x, warrior.y, 96, 96)
        pass

class Warrior:
    image = None
    effect = None

    def __init__(self):
        self.state_machine = StateMachine(self)
        self.frame = 0
        self.x, self.y = random.randint(1300 - 200, 1400), 73
        self.font = load_font('ENCR10B.TTF', 16)
        self.face_dir = -1
        self.hp = 200
        self.damage = 20
        self.score = 30
        self.attack = False
        self.state_machine.start(Run)
        self.zombie_hurt_bgm = load_wav('.\\Resources\\bgm\\zombie_hurt.mp3')
        self.zombie_hurt_bgm.set_volume(32)
        self.zombie_run_bgm = load_wav('.\\Resources\\bgm\\zombie_run.mp3')
        self.zombie_run_bgm.set_volume(15)
        self.zombie_attack_bgm = load_wav('.\\Resources\\bgm\\zombie_attack.mp3')
        self.zombie_attack_bgm.set_volume(10)
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle :      {time_out: Run, dead: Dead, hurt: Hurt},

                Run :       {find_attack: RunAttack, dead: Dead, hurt: Hurt},

                Hurt :      {time_out: Run, dead: Dead, hurt: Hurt},

                Attack_1 :  {time_out: Attack_2, miss: Run, dead: Dead, hurt: Hurt},

                Attack_2 :  {time_out: Attack_3, miss: Run, dead: Dead, hurt: Hurt},

                Attack_3 :  {time_out: Attack_1, miss: Run, dead: Dead, hurt: Hurt},

                RunAttack : {time_out: Attack_1, miss: Run, dead: Dead, hurt: Hurt},

                Dead: {}
            }
        )
        self.frame_rates = {
            'Idle': 5,
            'Run': 6,
            'Hurt': 2,
            'Attack_1': 4,
            'Attack_2': 4,
            'Attack_3': 3,
            'RunAttack': 4,
            'Dead': 4
        }

        if Warrior.image is None:
            Warrior.image = [
                load_image('.\\Resources\\monster\\Orc_Warrior\\Idle.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Run.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Hurt.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Attack_1.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Attack_2.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Attack_3.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Run+Attack.png'),
                load_image('.\\Resources\\monster\\Orc_Warrior\\Dead.png')
            ]

        if Warrior.effect is None:
            Warrior.effect = load_image('.\\Resources\\effect\\slash4\\png\\slash4_00007.png')

    def update(self):
        self.state_machine.update()
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
        if self.state_machine.cur_state != Dead:
            self.font.draw(self.x, self.y + 70, f'hp : {self.hp:02d}', (255, 0, 0))

    def get_bb(self, group):
        if group == 'boy:warrior_dic':
                return self.x - 2000, self.y - 1000, self.x, self.y + 1000
        if group == 'boy:warrior_attack':
            if self.face_dir == 1:
                if self.state_machine.cur_state == Attack_1:
                    return self.x + 50, self.y - 50, self.x - 10, self.y + 50
                elif self.state_machine.cur_state == Attack_2:
                    return self.x + 50, self.y - 50, self.x - 10, self.y + 50
                elif self.state_machine.cur_state == Attack_3:
                    return self.x + 50, self.y - 50, self.x - 10, self.y + 50
                elif self.state_machine.cur_state == RunAttack:
                    return self.x + 50, self.y - 50, self.x - 10, self.y + 50
                else:
                    return self.x + 50, self.y - 50, self.x - 10, self.y + 50
            elif self.face_dir == -1:
                if self.state_machine.cur_state == Attack_1:
                    return self.x - 50, self.y - 50, self.x + 10, self.y + 50
                elif self.state_machine.cur_state == Attack_2:
                    return self.x - 50, self.y - 50, self.x + 10, self.y + 50
                elif self.state_machine.cur_state == Attack_3:
                    return self.x - 50, self.y - 50, self.x + 10, self.y + 50
                elif self.state_machine.cur_state == RunAttack:
                    return self.x - 50, self.y - 50, self.x + 10, self.y + 50
                else:
                    return self.x - 50, self.y - 50, self.x + 10, self.y + 50
        if group == 'boy:warrior_find':
                return self.x - 150, self.y - 50, self.x + 150, self.y + 50
        else:
            return self.x - 28, self.y - 48, self.x + 28, self.y + 18

    def handle_collision(self, group, other, on):
        if self.state_machine.cur_state != Dead:
            if group == 'boy_attack:warrior' and on and other.attack:
                print(F'{group} collide {on}')
                self.state_machine.add_event(('HURT', 0))
                self.hp -= other.damage
                self.x += other.face_dir * 10
            if group == 'boy:warrior_find':
                if on:
                    if self.state_machine.cur_state == Run:
                        #print(F'{group} collide {on}')
                        self.state_machine.add_event(('FIND_ATTACK', 0))
                else:
                    if self.state_machine.cur_state in (Attack_1, Attack_2, Attack_3):
                        #print(F'{group} collide {on}')
                        self.state_machine.add_event(('MISS', 0))
            if group == 'boy:warrior_dic':
                #print(F'{group} collide {on}')
                if on:
                    if self.face_dir == 1:
                        self.face_dir = -1
                else:
                    if self.face_dir == -1:
                        self.face_dir = 1
        pass