import sys
import time
import requests
import configparser


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
    
    cur_frame = 0
    timer = 0

    try:
        print("Press CTRL-C to stop.")
        while True:
            frames = [home, player, weather, pet]
            timer += 1
            if timer >= 300:
                timer = 0
                cur_frame = (cur_frame + 1) % len(frames)
            frame = frames[cur_frame].generate()
            # frame = player.generate()
            # frame = weather.generate()
            # frame = pet.generate()

            if frame is None:
                frame = home.generate()
            
            matrix.SetImage(frame)
            time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit(0)

# Main function
if __name__ == "__main__":
    main()
