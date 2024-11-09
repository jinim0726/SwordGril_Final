from pico2d import load_image, get_time

from state_machine import (StateMachine, time_out, start_event, a_up, a_down, w_up, w_down
                           , s_up, s_down, d_up, d_down, j_up, j_down, hit, dead)


class Idle:
    @staticmethod
    def enter(boy, e):
        if a_up(e) or d_down(e) or time_out(e):
            boy.face_dir, boy.action = -1, 2
        elif d_up(e) or a_down(e) or start_event(e):
            boy.face_dir, boy.action = 1, 3
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()
        print('Boy Idle Enter')

    @staticmethod
    def exit(boy, e):
        print('Boy Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Run:
    @staticmethod
    def enter(boy, e):
        if d_down(e) or a_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif a_down(e) or d_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Jump:
    @staticmethod
    def enter(boy, e):
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

class Hurt:
    @staticmethod
    def enter(boy, e):
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

class Shield:
    @staticmethod
    def enter(boy, e):
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

class Attack_2:
    @staticmethod
    def enter(boy, e):
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

class Attack_3:
    @staticmethod
    def enter(boy, e):
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

class Attack_1:
    @staticmethod
    def enter(boy, e):
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

class Dead:
    @staticmethod
    def enter(boy, e):
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

class Boy:
    image = None

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 3
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            # 상태 변환 표기
            {
                Idle :      {a_down: Run, d_down: Run, a_up: Run, d_up: Run, s_down: Shield,
                                w_down: Jump, j_down: Attack_1, dead: Dead, hit: Hurt},

                Run :       {a_down: Idle, d_down: Idle, d_up: Idle, j_down: Attack_1,
                                w_down: Jump, a_up: Idle, s_down: Shield, dead: Dead, hit: Hurt},

                Jump :      {time_out: Idle, j_down: Attack_1,
                                s_down: Shield, dead: Dead},

                Hurt :      {time_out: Idle, dead: Dead},

                Shield :    {a_down: Run, d_down: Run, a_up: Run, d_up: Run, j_down: Attack_1,
                                s_up: Idle, w_down: Jump, dead: Dead},

                Attack_1 :  {time_out: Idle, j_down: Attack_2, s_down: Shield,
                                w_down: Jump, dead: Dead, hit: Hurt},

                Attack_2 :  {time_out: Idle, j_down: Attack_3, s_down: Shield,
                                w_down: Jump, dead: Dead, hit: Hurt},

                Attack_3 :  {time_out: Idle, j_down: Attack_1, s_down: Shield,
                                w_down: Jump, dead: Dead, hit: Hurt}
            }
        )
        self.frame_rates = {
            'Idle': 6,
            'Walk': 4,
            'Run': 8,
            'Jump': 12,
            'Hurt': 2,
            'Dead': 3,
            'Shield': 2,
            'Attack_1': 6,
            'Attack_2': 4,
            'Attack_3': 3
        }
        if Boy.image == None:
            Boy.image = {
            load_image('..\\Resources\\character\\Samurai\\Idle.png'),
            load_image('..\\Resources\\character\\Samurai\\Walk.png'),
            load_image('..\\Resources\\character\\Samurai\\Run.png'),
            load_image('..\\Resources\\character\\Samurai\\Jump.png'),
            load_image('..\\Resources\\character\\Samurai\\Hurt.png'),
            load_image('..\\Resources\\character\\Samurai\\Dead.png'),
            load_image('..\\Resources\\character\\Samurai\\Shield.png'),
            load_image('..\\Resources\\character\\Samurai\\Attack_1.png'),
            load_image('..\\Resources\\character\\Samurai\\Attack_2.png'),
            load_image('..\\Resources\\character\\Samurai\\Attack_3.png')
            }

    def update(self):
        self.state_machine.update()
        self.frame = (self.frame + 1) % 8

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.o, ('START', 0))

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )
        # INPUT : 실제입력이벤트값
        # TIME_OUT : 시간 종료
        # NONE : 없음..? 즉 IDLE상태인듯

    def draw(self):
        self.state_machine.draw()
