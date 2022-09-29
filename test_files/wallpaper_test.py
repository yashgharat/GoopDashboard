from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from datetime import datetime
from dateutil import tz

import time
import sys

bgs = {'spiderman' : Image.open('image_6.jpg').convert("RGB"),
        'castle' :   Image.open('image_5.jpg').convert("RGB")}

def main():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.brightness = 50
    options.gpio_slowdown = 2
    options.pwm_lsb_nanoseconds = 80
    options.limit_refresh_rate_hz = 150
    options.drop_privileges=False

    matrix = RGBMatrix(options = options)

    try:
        print("Press CTRL-C to stop.")
        while True:
            frame = generateCastle()

            matrix.SetImage(frame)
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.exit(0)

def generateCastle():
    currentTime = datetime.now(tz=tz.tzlocal())
    month = currentTime.month
    day = currentTime.day
    hours = currentTime.hour

    minutes = currentTime.minute
    seconds = currentTime.second

    frame = Image.open('image_4.jpg').convert("RGB").copy()

    return frame

main()