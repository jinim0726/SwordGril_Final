# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font, \
    draw_rectangle, KMOD_SHIFT, load_music, load_wav
import os

from sdl2 import SDL_GetModState, SDLK_j, SDL_SCANCODE_A, SDL_SCANCODE_D
import game_world
import game_framework
import gameover
import state_machine
from state_machine import (start_event, a_up, a_down, w_up, w_down, s_up, s_down,
                           d_up, d_down, j_up, j_down, hurt, dead, StateMachine, time_out, idle, run)

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.35
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

ACTION_PER_ATTACK = 1.0 / TIME_PER_ACTION


class Idle:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % boy.frame_rates['Idle']
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
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % boy.frame_rates['Run']
        boy.boy_walk_bgm.play(1)
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
        boy.current_frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        boy.boy_walk_bgm.play(1)
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % boy.frame_rates['Jump']
        boy.current_frame = boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time
        if boy.frame < (boy.frame_rates['Jump'] / 2):
            boy.x += boy.face_dir * RUN_SPEED_PPS / 2 * game_framework.frame_time
            boy.y += RUN_SPEED_PPS * game_framework.frame_time
        else:
            boy.x += boy.face_dir * RUN_SPEED_PPS / 2 * game_framework.frame_time
            boy.y -= RUN_SPEED_PPS * game_framework.frame_time

        if boy.current_frame >= boy.frame_rates['Jump']:
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
        boy.current_frame = 0
        boy.hp -= 10
        boy.combo = 0
        boy.boy_hurt_bgm.play(1)
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % boy.frame_rates['Hurt']
        boy.current_frame = boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time
        if boy.current_frame >= boy.frame_rates['Hurt']:
            boy.state_machine.add_event(('TIME_OUT', 0))
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
        if int(boy.frame) != 1:
            boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time) % boy.frame_rates['Shield']
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
        boy.current_frame = 0
        boy.attack_processed = False  # 공격 처리 완료 상태로 변경
        boy.boy_attack1_bgm.play(1)
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_ATTACK * game_framework.frame_time) % boy.frame_rates['Attack_1']
        boy.current_frame = boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 4  # 공격 처리를 원하는 프레임
        if not boy.attack_processed and int(boy.current_frame) == attack_frame:
            boy.attack = True
            boy.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            boy.attack = False

        if boy.current_frame >= boy.frame_rates['Attack_1']:
            boy.state_machine.add_event(('TIME_OUT', 0))
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
        boy.current_frame = 0
        boy.attack_processed = False  # 공격 처리 완료 상태로 변경
        boy.boy_attack2_bgm.play(1)
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_ATTACK * game_framework.frame_time) % boy.frame_rates['Attack_2']
        boy.current_frame = boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME * game_framework.frame_time

        attack_frame = 3  # 공격 처리를 원하는 프레임
        if not boy.attack_processed and int(boy.current_frame) == attack_frame:
            boy.attack = True
            boy.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            boy.attack = False

        if boy.current_frame >= boy.frame_rates['Attack_2']:
            boy.state_machine.add_event(('TIME_OUT', 0))
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
        boy.current_frame = 0
        boy.attack_processed = False  # 공격 처리 완료 상태로 변경
        boy.boy_attack1_bgm.play(1)
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_ATTACK * game_framework.frame_time) % boy.frame_rates['Attack_3']
        boy.current_frame = boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        # 특정 프레임에서만 공격 처리
        attack_frame = 2  # 공격 처리를 원하는 프레임
        if not boy.attack_processed and int(boy.current_frame) == attack_frame:
            boy.attack = True
            boy.attack_processed = True  # 공격 처리 완료 상태로 변경
        else:
            boy.attack = False

        # 애니메이션 종료 시 이벤트 추가
        if boy.current_frame >= boy.frame_rates['Attack_3']:
            boy.state_machine.add_event(('TIME_OUT', 0))
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
        game_framework.change_mode(gameover)
        pass

    @staticmethod
    def exit(boy, e):
        #if space_down(e): boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image[9].clip_draw(int(boy.frame) * 128, 0, 128, 128, boy.x, boy.y)
        else:
            boy.image[9].clip_composite_draw(int(boy.frame) * 128, 0, 128, 128, 0, 'h', boy.x, boy.y, 128, 128)
        pass

class ToIdleOrRun:
    @staticmethod
    def enter(boy, e):
        if state_machine.is_key_pressed(SDL_SCANCODE_A) and state_machine.is_key_pressed(SDL_SCANCODE_D):  # A 키 확인
            boy.state_machine.add_event(('TO_IDLE', 0))
        elif state_machine.is_key_pressed(SDL_SCANCODE_A) or state_machine.is_key_pressed(SDL_SCANCODE_D):
            boy.state_machine.add_event(('TO_RUN', 0))
        else:
            boy.state_machine.add_event(('TO_IDLE', 0))
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        pass

class Left:
    @staticmethod
    def enter(boy, e):
        boy.face_dir = -1
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.face_dir = -1
        pass

    @staticmethod
    def draw(boy):
        pass

class Right:
    @staticmethod
    def enter(boy, e):
        boy.face_dir = 1
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.face_dir = 1
        pass

    @staticmethod
    def draw(boy):
        pass

class Boy:
    image = None

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.combo = 0
        self.frame = 0
        self.current_frame = 0
        self.hp = 200
        self.damage = 20
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.dic_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.dic_machine.start(Right)
        self.attack = False
        self.boy_walk_bgm = load_wav('.\\Resources\\bgm\\boy_walk.mp3')
        self.boy_walk_bgm.set_volume(1)
        self.boy_attack1_bgm = load_wav('.\\Resources\\bgm\\boy_attack1.mp3')
        self.boy_attack1_bgm.set_volume(10)
        self.boy_attack2_bgm = load_wav('.\\Resources\\bgm\\boy_attack2.mp3')
        self.boy_attack2_bgm.set_volume(10)
        self.boy_shield_bgm = load_wav('.\\Resources\\bgm\\boy_shield.mp3')
        self.boy_shield_bgm.set_volume(10)
        self.boy_hurt_bgm = load_wav('.\\Resources\\bgm\\boy_hurt.mp3')
        self.boy_hurt_bgm.set_volume(10)
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle :      {a_down: Run, a_up: Run, d_down: Run, d_up: Run, s_down: Shield,
                                w_down: Jump, j_down: Attack_1, dead: Dead, hurt: Hurt},

                Run :       {a_down: Idle, a_up: Idle, d_down: Idle, d_up: Idle, j_down: Attack_1,
                                w_down: Jump, s_down: Shield, dead: Dead, hurt: Hurt},

                Jump :      {time_out: ToIdleOrRun, dead: Dead},

                Hurt :      {time_out: ToIdleOrRun, dead: Dead},

                Shield :    {s_up: ToIdleOrRun, dead: Dead},

                Attack_1 :  {time_out: Attack_2, j_up: ToIdleOrRun, dead: Dead, hurt: Hurt},

                Attack_2 :  {time_out: Attack_3, j_up: ToIdleOrRun, dead: Dead, hurt: Hurt},

                Attack_3 :  {time_out: Attack_1, j_up: ToIdleOrRun, dead: Dead, hurt: Hurt},

                Dead : {},

                ToIdleOrRun : {idle: Idle, run: Run, dead: Dead}
            }
        )
        self.dic_machine.set_transitions(
            {
                Right : {a_down: Left, d_up: Left},
                Left : {d_down: Right, a_up: Right}
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
        if Boy.image is None:
            print("Current working directory:", os.getcwd())
            Boy.image = [
            load_image('.\\Resources\\character\\Samurai\\Idle.png'),
            load_image('.\\Resources\\character\\Samurai\\Walk.png'),
            load_image('.\\Resources\\character\\Samurai\\Run.png'),
            load_image('.\\Resources\\character\\Samurai\\Jump.png'),
            load_image('.\\Resources\\character\\Samurai\\Hurt.png'),
            load_image('.\\Resources\\character\\Samurai\\Shield.png'),
            load_image('.\\Resources\\character\\Samurai\\Attack_1.png'),
            load_image('.\\Resources\\character\\Samurai\\Attack_2.png'),
            load_image('.\\Resources\\character\\Samurai\\Attack_3.png'),
            load_image('.\\Resources\\character\\Samurai\\Dead.png')
            ]

    def update(self):
        self.state_machine.update()
        self.dic_machine.update()
        self.damage = 20 + (self.combo * 10)
        if self.hp <= 0 and self.state_machine.cur_state != Dead:
            self.state_machine.add_event(('DEAD', 0))

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        if self.state_machine.cur_state != Dead:
            self.dic_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        # 충돌 영역 그리기
        self.font.draw(self.x, self.y + 50, f'combo : {self.combo:02d}', (255, 255, 0))
        self.font.draw(self.x, self.y + 70, f'hp : {self.hp:02d}', (255, 255, 0))

    def get_bb(self, group):
        if group == 'boy_attack:berserk':
            if self.face_dir == 1:
                return self.x - 30, self.y - 70, self.x + 85, self.y + 20
            else:
                return self.x - 85, self.y - 70, self.x + 30, self.y + 20
        else:
            return self.x - 20, self.y - 70, self.x + 20, self.y + 20
        pass

    def handle_collision(self, group, other, on):
        # fill here
        if group == 'boy:berserk_attack' and on and other.attack:
            print(F'{group} collide {on}')
            if self.state_machine.cur_state == Shield:
                self.boy_shield_bgm.play(1)
                self.combo += 1
            else:
                self.state_machine.add_event(('HURT', 0))
                self.hp -= other.damage
                self.combo = 0
        if group == 'boy_attack:berserk' and on and self.attack and other.hp > 0:
            self.combo += 1
            print(F'{group} collide {on}')
        if group == 'boy:warrior_attack' and on and other.attack:
            print(F'{group} collide {on}')
            if self.state_machine.cur_state == Shield:
                self.combo += 1
            else:
                self.hp -= other.damage
                self.combo = 0
        if group == 'boy_attack:warrior' and on and self.attack and other.hp > 0:
            self.combo += 1
            print(F'{group} collide {on}')
        pass