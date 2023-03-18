import random
import requests
import schedule

from datetime import datetime
from json import loads, dumps
from PIL import Image, ImageFont, ImageDraw

from modules import weather_module

class WeatherScreen():
    def __init__(self, path="../assets/weather/weather_anim.png"):
        self.path = path
        self.fonts = {}
        self.fonts['temp'] = ImageFont.truetype("../fonts/tiny.otf", 7)
        self.fonts['city'] = ImageFont.truetype("../fonts/tiny.otf", 6)
        self.fonts['info'] = ImageFont.truetype("../fonts/tiny.otf", 5)

        self.location_animation_cnt = 0
        self.sun_animation_cnt = 0
        self.rock_animation_cnt = 0

        self.canvas_width = 64
        self.canvas_height = 32
        self.font_color = (255, 255, 255)

        self.anim_frame = 0
        self.anim_dict = self.load_weather()
        self.cur_anim_key = ''

        self.wittr = weather_module.WeatherModule()
        self.cur_condition = ''
        self.response = self.wittr.getCurrentWeather()

    def getWeatherKey(self, condition):        
        desc = condition['weatherDesc'][0]['value']
        feels_like = int(condition['FeelsLikeF'])
        precip = float(condition['precipInches'])
        visibility = float(condition['visibility'])
        wind = float(condition['windspeedMiles'])
        sunset = datetime.strptime(condition['sunset'][:-3], '%H:%M')


        if(desc == 'Sunny'):
            return 'Hot' if(feels_like > 94) else 'Sunny'
        if(feels_like < 50): return 'Snowy'
        if(desc.lower().contains("showers") or desc.lower().contains('rain') or precip > 5):
            return 'Rainy'
        if(desc.lower().contains('Cloudy') and precip < 5):
            return 'Cloudy'
        if(desc == 'Fog' or visibility < .3):
            return 'Foggy'
        if(wind > 25):
            return 'Floating'
        if(desc.lower().contains("thundery")):
            return 'Stormy'
        if(datetime.now()<sunset):
            return 'Night'
        
        return 'Sunny'
    
    def populateWeather(self):
        self.response = self.wittr.getCurrentWeather()

    def generate(self):
        BUFFER = 1
        Y_LOC = BUFFER
        schedule.every(2).hours.do(self.populateWeather)
        if self.response is not None:
            if (self.cur_condition != self.response):
                self.cur_condition = self.response
                self.location_animation_cnt = 0
                self.sun_animation_cnt = 0
                self.rock_animation_cnt = 0
                self.cur_anim_key = self.getWeatherKey(self.response)

            frame = Image.new(
                "RGB", (self.canvas_width, self.canvas_height), (0, 0, 0))
            draw = ImageDraw.Draw(frame)

            temp = self.cur_condition['temp_F']
            temp_width, temp_height = self.fonts['temp'].getsize(temp)
            draw.text(((32+((32-temp_width)/2)), Y_LOC),
                      temp, font=self.fonts['temp'])

            Y_LOC += temp_height + (BUFFER*2)
            location = self.cur_condition['location']
            location_width, location_height = self.fonts['city'].getsize(
                location)

            if location_width > 31:
                spacer = "   "
                draw.text((34-self.location_animation_cnt, Y_LOC),
                          location + spacer + location, font=self.fonts['city'])
                self.location_animation_cnt += 1
                if self.location_animation_cnt == self.fonts['city'].getsize(location + spacer)[0]:
                    self.location_animation_cnt = 0
            else:
                draw.text(((32+((32-location_width)/2)), Y_LOC),
                          location, font=self.fonts['city'])

            Y_LOC += location_height + (BUFFER*2)
            precip = self.cur_condition['precipInches']
            precip_width, precip_height = self.fonts['info'].getsize(precip)

            feels_like = self.cur_condition['FeelsLikeF']
            feels_like_width, feels_like_height = self.fonts['info'].getsize(
                feels_like)

            spacing = int((32-(precip_width+feels_like_width))/5)
            string_build = precip + (' ' * spacing) + feels_like
            draw.text(((31+spacing), Y_LOC), string_build,
                      font=self.fonts['info'])

            Y_LOC += max(feels_like_height, precip_height) + (BUFFER*2)
            sunrise = self.cur_condition['sunrise'][:-3]
            sunrise_width, sunrise_height = self.fonts['info'].getsize(sunrise)

            sunset = self.cur_condition['sunset'][:-3]
            sunset_width, sunset_height = self.fonts['info'].getsize(sunset)

            string_build = sunrise + ' ' + sunset

            spacer = "   "
            draw.text((34-self.sun_animation_cnt, Y_LOC), string_build +
                      spacer + string_build, font=self.fonts['info'])
            self.sun_animation_cnt += 1
            if self.sun_animation_cnt == self.fonts['info'].getsize(string_build + spacer)[0]:
                self.sun_animation_cnt = 0

            # draw.rectangle((32,0,33,32), fill=(0,0,0))
            frame.paste(self.anim_dict[self.cur_anim_key][self.rock_animation_cnt], (0, 0))
            self.rock_animation_cnt += 1
            if self.rock_animation_cnt == len(self.anim_dict[self.cur_anim_key]):
                self.rock_animation_cnt = 0

        return frame

    def load_weather(self):
        sheet = Image.open(self.path)
        width, height = sheet.size
        anim_sprites = []
        anim_keys = ['Cloudy', 'Floating', 'Foggy', 'Hot',
                     'Night', 'Rainy', 'Snowy', 'Stormy', 'Sunny']

        for y in range(0, height, 32):
            cur_anim = []
            for x in range(0, width, 32):
                sprite = sheet.crop((x, y, x+32, y+32))
                if sprite.getbbox() is not None:
                    cur_anim.append(sprite)
            anim_sprites.append(cur_anim)

        return dict(zip(anim_keys, anim_sprites))
