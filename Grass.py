from pico2d import *

class Grass:
    First = None
    Second = None
    Third = None
    Fourth = None

    def __init__(self):
        if Grass.First == None:
           Grass.First = [
               load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_01\\Cartoon_Forest_BG_01.png'),
               load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_01\\Layers\\Ground.png')
           ]
        if Grass.Second == None:
            Grass.Second = [
                load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_02\\Cartoon_Forest_BG_02.png'),
                load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_02\\Layers\\Ground.png')
            ]
        if Grass.Third == None:
            Grass.Third = [
                load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_03\\Cartoon_Forest_BG_03.png'),
                load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_03\\Layers\\Ground.png')
            ]
        if Grass.Fourth == None:
            Grass.Fourth = [
                load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_04\\Cartoon_Forest_BG_04.png'),
                load_image('..\\SwordGirl_3\\Resources\\UI\\Cartoon_Forest_BG_04\\Layers\\Ground.png')
            ]


    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # fill here
        return 0, 0, 1600 - 1, 50

