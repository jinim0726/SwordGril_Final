from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_j, SDL_GetKeyboardState

def is_key_pressed(key):
    keys = SDL_GetKeyboardState(None)
    return keys[key]

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
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_j)

def time_out(e):
    return (e[0] == 'TIME_OUT')

def idle(e):
    return(e[0] == 'TO_IDLE')

def run(e):
    return(e[0] == 'TO_RUN')

def hurt(e):
    return (e[0] == 'HURT')

def dead(e):
    return (e[0] == 'DEAD')

def find_run(e):
    return (e[0] == 'FIND_RUN')

def find_attack(e):
    return (e[0] == 'FIND_ATTACK')

def miss(e):
    return (e[0] == 'MISS')

def none(e):
    return (e[0] == 'NONE')


class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def start(self, state):
        self.cur_state = state

        print(f'Enter into {state}')
        self.cur_state.enter(self.o, ('START', 0))

    def add_event(self, e):
        # print(f'    DEBUG: New event {e} added to event Que')
        self.event_que.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                print(f'Exit from {self.cur_state}')
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                print(f'Enter into {self.cur_state}')
                self.cur_state.enter(self.o, e)
                return

        # print(f'        Warning: Event [{e}] at State [{self.cur_state}] not handled')
