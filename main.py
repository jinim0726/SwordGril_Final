from pico2d import open_canvas, delay, close_canvas
import game_framework
import os

import title_mode as start_mode

print(os.getenv('PYSDL2_DLL_PATH'))
open_canvas(1067, 600)
game_framework.run(start_mode)
close_canvas()