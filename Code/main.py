from pico2d import *
import time

class Manage_World:
    def reset_world(self):
        pass

    def update_world(self):
        pass

    def render_world(self):
        clear_canvas()
        update_canvas()


class Character:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 0 # -1 for left, 1 for right
        self.action = 0  # Start in Idle state
        self.hp = 100  # Health Points
        self.attack_power = 10  # Damage dealt to enemies
        # 0:Idle, 1:Walk, 2:Run, 3:Jump, 4:Hurt, 5:Dead, 6:Shield, 7-9:Attack_1/2/3
        self.is_jumping = False
        self.is_running = False
        self.is_attacking = False
        self.is_shielding = False
        self.attack_stage = 0  # 0: No attack, 1: Attack_1, 2: Attack_2, 3: Attack_3
        self.attack_start_time = 0
        # Timing control to make all animations have consistent duration (~1-2 seconds)
        self.animation_duration = 1.5  # Animation duration in seconds
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
        self.start_time = time.time()

        self.image_Idle = load_image('..\\Resources\\character\\Samurai\\Idle.png')
        self.image_Walk = load_image('..\\Resources\\character\\Samurai\\Walk.png')
        self.image_Run = load_image('..\\Resources\\character\\Samurai\\Run.png')
        self.image_Jump = load_image('..\\Resources\\character\\Samurai\\Jump.png')
        self.image_Hurt = load_image('..\\Resources\\character\\Samurai\\Hurt.png')
        self.image_Dead = load_image('..\\Resources\\character\\Samurai\\Dead.png')
        self.image_Shield = load_image('..\\Resources\\character\\Samurai\\Shield.png')
        self.image_Attack_1 = load_image('..\\Resources\\character\\Samurai\\Attack_1.png')
        self.image_Attack_2 = load_image('..\\Resources\\character\\Samurai\\Attack_2.png')
        self.image_Attack_3 = load_image('..\\Resources\\character\\Samurai\\Attack_3.png')

    def draw(self):
        if self.action == 0:
            self.image_Idle.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 1:
            self.image_Walk.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 2:
            self.image_Run.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 3:
            self.image_Jump.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 4:
            self.image_Hurt.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 5:
            self.image_Dead.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 6:
            self.image_Shield.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 7:
            self.image_Attack_1.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 8:
            self.image_Attack_2.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)
        elif self.action == 9:
            self.image_Attack_3.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 256, 256)

    def update(self):
        # Update frame based on time to maintain consistent animation duration
        elapsed = time.time() - self.start_time
        frame_count = self.frame_rates[list(self.frame_rates.keys())[self.action]]
        total_duration = self.animation_duration
        frame_duration = total_duration / frame_count

        if elapsed >= frame_duration:
            self.frame = (self.frame + 1) % frame_count
            self.start_time = time.time()

        # Check character state and update action
        if self.is_attacking:
            # Handle combo attack stages
            if time.time() - self.attack_start_time > 0.5:
                self.attack_stage = (self.attack_stage % 3) + 1
                self.action = 6 + self.attack_stage
                self.attack_start_time = time.time()

        if self.hp <= 0:
            self.action = 5  # Dead state

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.action = 1  # Walk state
                self.dir = 1
            elif event.key == SDLK_LEFT:
                self.action = 1  # Walk state
                self.dir = -1
            elif event.key == SDLK_UP:
                self.action = 2  # Run state
            elif event.key == SDLK_SPACE:
                self.action = 3  # Jump state
            elif event.key == SDLK_a:
                self.action = 7  # Attack 1 state
            elif event.key == SDLK_s:
                self.action = 8  # Attack 2 state
            elif event.key == SDLK_d:
                self.action = 9  # Attack 3 state
            elif event.key == SDLK_z:
                self.action = 6  # Shield state

        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT, SDLK_UP):
                self.action = 0  # Return to Idle state
                self.dir = 0

        # Check character state and update action
        if self.is_attacking:
            # Handle combo attack stages
            if time.time() - self.attack_start_time > 0.5:
                self.attack_stage = (self.attack_stage % 3) + 1
                self.action = 6 + self.attack_stage
                self.attack_start_time = time.time()

        if self.hp <= 0:
            self.action = 5  # Dead state

    def take_damage(self, damage):
        if not self.is_shielding:
            self.hp -= damage
            if self.hp > 0:
                self.action = 4  # Hurt state
            else:
                self.action = 5  # Dead state

    def attack(self):
        if not self.is_shielding and not self.is_attacking:
            self.is_attacking = True
            self.attack_stage = 1
            self.action = 7
            self.attack_start_time = time.time()

    def move(self, direction, is_running=False):
        if not self.is_shielding and not self.is_attacking:
            self.dir = direction
            self.is_running = is_running
            if is_running:
                self.action = 2  # Run state
            else:
                self.action = 1  # Walk state
            self.x += direction * (5 if is_running else 2)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.action = 3  # Jump

    def shield(self, active):
        self.is_shielding = active
        if active:
            self.action = 6
        elif self.action == 6:
            self.action = 0  # Return to Idle if shield is released

class Monster:
    def __init__(self):
        self.image = load_image('grass.png')

class BackGround:
    def __init__(self):
        self.image = load_image('grass.png')

def handle_events(character):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            close_canvas()
            exit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                character.move(-1, is_running=character.is_running)
            elif event.key == SDLK_d:
                character.move(1, is_running=character.is_running)
            elif event.key == SDLK_LSHIFT or event.key == SDLK_RSHIFT:
                character.is_running = True
            elif event.key == SDLK_w:
                character.jump()
            elif event.key == SDLK_s:
                character.shield(True)
            elif event.key == SDLK_j:
                character.attack()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a or event.key == SDLK_d:
                character.move(0)  # Stop moving
            elif event.key == SDLK_LSHIFT or event.key == SDLK_RSHIFT:
                character.is_running = False
            elif event.key == SDLK_s:
                character.shield(False)


def main():
    open_canvas(800, 600)

    # Create the game objects
    character = Character()

    # Game loop
    while character.hp > 0:
        handle_events(character)

        # Update game state
        character.update()

        # Render game world
        clear_canvas()
        character.draw()
        update_canvas()

        # Frame delay
        delay(0.03)  # ~30 FPS

    # Character is dead, handle game over scenario
    while True:
        clear_canvas()
        character.draw()  # Draw the character in a dead state
        update_canvas()
        handle_events(character)  # Allow quitting the game

    close_canvas()


if __name__ == '__main__':
    main()
