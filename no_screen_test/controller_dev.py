import configparser
import requests
import time
import sys

import spotify_player_dev
import home_screen_dev
import pet_screen_dev
import weather_screen_dev
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

def main():
    config = configparser.ConfigParser()
    parsed_configs = config.read('../config.ini')
    if len(parsed_configs) == 0:
        print("no config file found")
        sys.exit()

    options = RGBMatrixOptions()
    options.cols=64
    options.pwm_lsb_nanoseconds = 80
    options.limit_refresh_rate_hz = 150
    # options.pixel_style = 'square'
    matrix = RGBMatrix(options = options)

    home = home_screen_dev.HomeScreen()
    player = spotify_player_dev.SpotifyScreen(config)
    pet = pet_screen_dev.PetScreen()
    weather = weather_screen_dev.WeatherScreen()

    try:
        print("Press CTRL-C to stop.")
        while True:
            # frame = home.generate()
            # frame = player.generate()
            frame = weather.generate()
            # frame = pet.generate()

            if frame is None:
                frame = pet.generate()
            
            matrix.SetImage(frame)
            time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit(0)

# Main function
if __name__ == "__main__":
    main()
