import requests
from json import loads, dumps

class WeatherModule:
    def __init__(self):
        self.url = 'https://wttr.in?format=j1'
        self.cur_condition = ''

    def getCurrentWeather(self):
        try:
            r = requests.get(self.url)
            if r.status_code == 200:
                obj = loads(r.text)
                if len(obj) > 0:
                    self.cur_condition = obj['current_condition'][0]
                    sunset = obj['weather'][0]['astronomy'][0]['sunset']
                    del(obj)
                    self.cur_condition['sunset'] = sunset
                return self.cur_condition
            else:
                return None
        except Exception as e:
            print(e)
            return None