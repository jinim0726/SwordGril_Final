# event ( 종류 문자열 , 실제 값 )
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_j


def start_event(e):
    return e[0] == 'START'

def w_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w)

def w_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w)

def a_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a)

def a_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a)

def s_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s)

def s_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s)

def d_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d)

def d_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d)

def j_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j)

def j_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j)

def time_out(e):
    return (e[0] == 'TIME_OUT')

def hit(e):
    return (e[0] == 'Hit')

def dead(e):
    return (e[0] == 'DEAD')

def none(e):
    return (e[0] == 'NONE')


class StateMachine:

     def __init__(self, o):
         # 담당 객체 할당 ( boy의 self가 전달 )
        self.o = o # self.0는 상태머신과 연결된 캐릭터 자체
        self.event_que = [] # 발생하는 이벤트를 담는 곳
         # 파이썬은 함수 호출에 있어서 굉장히 자유롭다.

     def start(self, start_state):
         # 현재 상태를 시작 상태로 만듬
        self.cur_state = start_state
        self.cur_state.enter(self.o, ('START', 0))
        print(f'ENTER into {self.cur_state}')

     def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            e = self.event_que.pop(0) # 이벤트 큐에 뭔가 있으면 그거 꺼냄
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): # e가 지금 check_event이면
                    self.cur_state.exit(self.o, e)
                    print(f'EXIT from {self.cur_state}.')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e) # 새로운 상태 진입!
                    print(f'ENTER into {next_state}.')
                    return

     def draw(self):
        self.cur_state.draw(self.o)

     def set_transitions(self, transitions):
         self.transitions = transitions

     def add_event(self, e):
         self.event_que.append(e) # 상태머신용 이벤트 추가
         print(f'      DEBUG: new event {e} is added.')