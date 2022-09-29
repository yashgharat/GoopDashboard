import configparser
import requests
import time
import sys

import spotify_player_dev
import home_screen_dev
import goop_screen_dev
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
    matrix = RGBMatrix(options = options)

    player = spotify_player_dev.SpotifyScreen(config)
    home = home_screen_dev.HomeScreen()
    goop = goop_screen_dev.GoopScreen()

    try:
        print("Press CTRL-C to stop.")
        while True:
            frame = player.generate()
            # frame = goop.generate()
            # frame = home.generate()

            if frame is None:
                frame = goop.generate()
            
            matrix.SetImage(frame)
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.exit(0)

# Main function
if __name__ == "__main__":
    main()
