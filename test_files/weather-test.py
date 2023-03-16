import requests
import json

r = requests.get("https://wttr.in?format=j1")
obj = json.loads(r.text)
cur_condition = obj['current_condition'][0]
sunset = obj['weather'][0]['astronomy'][0]['sunset']
sunrise = obj['weather'][0]['astronomy'][0]['sunrise']
location = obj['nearest_area'][0]['areaName'][0]['value']
cur_condition['sunset'] = sunset
cur_condition['sunrise'] = sunrise
cur_condition['location'] = location
del(obj)

print(json.dumps(cur_condition, indent=2))


