from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from dateutil import tz

import requests
import time

light_pink = (255,219,218)
dark_pink = (219,127,142)
white = (230,255,255)

class HomeScreen():
    def __init__(self):
        self.days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.font = ImageFont.truetype("../fonts/tiny.otf", 5)
        self.canvas_width = 64
        self.canvas_height = 32
        self.cycle_time = 20
        self.use_24_hour = False

        self.lastGenerateCall = None
        self.on_cycle = True

        self.bgs = {'sakura' : Image.open('../assets/backgrounds/sakura-bg.png').convert("RGB")}

        self.currentIdx = 0

    def generate(self):
        frame = self.generateSakura()
        return frame

    def generateSakura(self):
        currentTime = datetime.now(tz=tz.tzlocal())
        month = currentTime.month
        day = currentTime.day
        dayOfWeek = self.days[currentTime.weekday()]
        hours = currentTime.hour
        if not self.use_24_hour:
            hours = hours % 12
            if (hours == 0):
                hours += 12 
        minutes = currentTime.minute

        frame = self.bgs['sakura'].copy()
        draw = ImageDraw.Draw(frame)

        draw.text((3, 6), padToTwoDigit(hours), light_pink, font=self.font)
        draw.text((10, 6), ":", light_pink, font=self.font)
        draw.text((13, 6), padToTwoDigit(minutes), light_pink, font=self.font)

        draw.text((23, 6), padToTwoDigit(month), dark_pink, font=self.font)
        draw.text((30, 6), ".", dark_pink, font=self.font)
        draw.text((33, 6), padToTwoDigit(day), dark_pink, font=self.font)

        draw.text((18, 12), dayOfWeek, dark_pink, font=self.font)
        
        return frame
        
def padToTwoDigit(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)