import random
import requests

from json import loads, dumps
from PIL import Image, ImageFont, ImageDraw
from time import sleep
from modules import weather_module

class WeatherScreen():
    def __init__(self, path="../assets/weather/weather_anim.png"):
        self.path = path
        self.fonts = {}
        self.fonts['temp'] = ImageFont.truetype("../fonts/tiny.otf", 7)
        self.fonts['city'] = ImageFont.truetype("../fonts/tiny.otf", 3)
        self.fonts['info'] = ImageFont.truetype("../fonts/tiny.otf", 2)

        self.canvas_width = 64
        self.canvas_height = 32
        self.font_color = (255,255,255)

        self.anim_frame = 0
        self.cur_anim = []
        self.anim_dict = self.load_weather()

        self.wittr = weather_module.WeatherModule()
        self.cur_condition = ''
    
    def generate(self):
        response = self.wittr.getCurrentWeather()
        if response is not None:
            if(self.cur_condition != response):
                self.cur_condition = response
            
            frame = Image.new("RGB", (self.canvas_width, self.canvas_height), (0,0,0))
            draw = ImageDraw.Draw(frame)

            draw.text((42, 2), self.cur_condition['temp_F'], font=self.fonts['temp'])
            draw.text((42, 2), self.cur_condition['temp_F'], font=self.fonts['temp'])

            draw.rectangle((32,0,33,32), fill=(0,0,0))
            frame.paste(self.anim_dict['Floating'][3], (0,0))

        return frame

    def load_weather(self):
        sheet = Image.open(self.path)
        width, height = sheet.size
        anim_sprites = []
        anim_keys = ['Cloudy', 'Floating', 'Foggy', 'Hot', 'Night', 'Rainy', 'Snowy', 'Stormy', 'Sunny']

        for y in range(0, height, 32):
            cur_anim = []
            for x in range(0, width, 32):
                sprite = sheet.crop((x, y, x+32, y+32))
                if sprite.getbbox() is not None:
                    cur_anim.append(sprite)
            anim_sprites.append(cur_anim)
        
        return dict(zip(anim_keys, anim_sprites))
        

                    