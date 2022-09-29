import configparser
import requests
import time
import sys
from io import BytesIO

from modules import weather_module
import spotify_player
import home_screen


from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

import warnings
warnings.filterwarnings('ignore')

def main():
    config = configparser.ConfigParser()
    parsed_configs = config.read('config.ini')
    if len(parsed_configs) == 0:
        print("no config file found")
        sys.exit()
    
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.brightness = 50
    options.gpio_slowdown = 2
    options.pwm_lsb_nanoseconds = 80
    options.limit_refresh_rate_hz = 150
    options.drop_privileges=False

    matrix = RGBMatrix(options = options)

    player = spotify_player.SpotifyScreen(config)
    weather = weather_module.WeatherModule(config)

    print(weather.getWeather())

    home = home_screen.HomeScreen()

    try:
        print("Press CTRL-C to stop.")
        while True:
            frame = player.generate()

            if frame is None:
                frame = home.generate()

            matrix.SetImage(frame)
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.exit(0)

main()
