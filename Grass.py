from pico2d import *

import game_framework
import gameclear

class Grass:
    Image = None
    stage = 0
    score = 0
    spawn_time = 0
    MONSTER_SPAWN_INTERVAL = 5.0  # 몬스터가 생성되는 간격 (초)
    BERSERK_COUNT = 1
    WARRIOR_COUNT = 1

    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 30)
        self.x, self.y = 534, 300
        self.bgm = load_music('.\\Resources\\bgm\\background.mp3')
        self.bgm.set_volume(32)

        if Grass.Image == None:
           Grass.Image = [
               load_image('.\\Resources\\UI\\Cartoon_Forest_BG_01\\Cartoon_Forest_BG_01.png'),
               load_image('.\\Resources\\UI\\Cartoon_Forest_BG_02\\Cartoon_Forest_BG_02.png'),
               load_image('.\\Resources\\UI\\Cartoon_Forest_BG_03\\Cartoon_Forest_BG_03.png'),
               load_image('.\\Resources\\UI\\Cartoon_Forest_BG_04\\Cartoon_Forest_BG_04.png')
           ]

    def update(self):
        if self.score >= 800:
            game_framework.change_mode(gameclear)
        elif self.score >= 400:
            self.stage = 3
            self.MONSTER_SPAWN_INTERVAL = 3.5
            self.BERSERK_COUNT = 2
            self.WARRIOR_COUNT = 1
        elif self.score >= 200:
            self.stage = 2
            self.MONSTER_SPAWN_INTERVAL = 4.0
            self.BERSERK_COUNT = 2
            self.WARRIOR_COUNT = 1
        elif self.score >= 50:
            self.stage = 1
            self.MONSTER_SPAWN_INTERVAL = 4.5
            self.BERSERK_COUNT = 2
            self.WARRIOR_COUNT = 1
        pass

    def draw(self):
        self.Image[self.stage].clip_composite_draw(0, 0, 1920, 1080, 0, '', self.x, self.y, 1067, 600)
        self.font.draw(self.x - 100, self.y + 230, f'STAGE : {self.stage:02d}', (255, 255, 0))
        self.font.draw(self.x - 100, self.y + 250, f'SCORE : {self.score:02d}', (255, 255, 0))

    def get_bb(self):
        # fill here
        return 0, 0, 1600 - 1, 50

