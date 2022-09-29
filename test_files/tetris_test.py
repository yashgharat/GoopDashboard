import cv2
import sys
import time
import numpy as np
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# sys.path.insert(1, '/home/yashgharat12/my-dash/')
sys.path.insert(1, '/home/syre/my-dash/')
from modules import tetris_module as tetris

options = RGBMatrixOptions()
options.cols = 64
options.brightness = 50
options.gpio_slowdown =  1.0

matrix = RGBMatrix(options = options)
double_buffer = matrix.CreateFrameCanvas()

canvas_w = 32
canvas_h = 32

tetris.make_canvas(canvas_h, canvas_w , 0)
now = time.strftime('%I %M', time.localtime(time.time()))

tetris.set_scale(2)
tetris.set_bottom_shift(0)
tetris_str2 = tetris.TetrisString(0, 0,  now)
tetris_str2.animate(matrix, double_buffer)



time.sleep(10)