import requests
import time

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from modules import spotify_module

import warnings
warnings.filterwarnings('ignore')

class SpotifyScreen:
    def __init__(self, config):
        self.font = ImageFont.truetype("../fonts/tiny.otf", 5)
        
        self.canvas_width = 64
        self.canvas_height = 32
        self.title_color = (255,255,255)
        self.artist_color = (255,255,255)
        self.album_color = (255,255,255)
        self.play_color = (255,255,255)

        self.current_art_url = ''
        self.current_art_img = None
        self.current_title = ''
        self.current_artist = ''
        self.current_album = ''

        self.title_animation_cnt = 0
        self.artist_animation_cnt = 0
        self.album_animation_cnt = 0

        self.is_playing = False

        self.spot = spotify_module.SpotifyModule(config)
    
    def generate(self):
        response = self.spot.getCurrentPlayback()
        if response is not None:
            #return (artist, title, art_url, self.isPlaying, track["item"]["uri"])
            (artist,title,art_url,self.is_playing,album, _) = response

            if (self.current_title != title or self.current_artist != artist or self.current_album != album):
                self.current_artist = artist
                self.current_title = title
                self.current_album = album

                self.title_animation_cnt = 0
                self.artist_animation_cnt = 0
                self.album_animation_cnt = 0

            if self.current_art_url != art_url:
                self.current_art_url = art_url
                response = requests.get(self.current_art_url)
                img = Image.open(BytesIO(response.content))
                self.current_art_img = img.resize((self.canvas_height, self.canvas_height), resample=Image.LANCZOS)

            frame = Image.new("RGB", (self.canvas_width, self.canvas_height), (0,0,0))
            draw = ImageDraw.Draw(frame)

            title_len = self.font.getsize(self.current_title)[0]
            if title_len > 31:
                spacer = "   "
                draw.text((34-self.title_animation_cnt, 0), self.current_title + spacer + self.current_title, self.title_color, font = self.font)
                self.title_animation_cnt += 1
                if self.title_animation_cnt == self.font.getsize(self.current_title + spacer)[0]:
                    self.title_animation_cnt = 0
            else:
                draw.text((34-self.title_animation_cnt, 0), self.current_title, self.title_color, font = self.font)

            artist_len = self.font.getsize(self.current_artist)[0]
            if artist_len > 31:
                spacer = "     "
                draw.text((34-self.artist_animation_cnt, 7), self.current_artist + spacer + self.current_artist, self.artist_color, font = self.font)
                self.artist_animation_cnt += 1
                if self.artist_animation_cnt == self.font.getsize(self.current_artist + spacer)[0]:
                    self.artist_animation_cnt = 0
            else:
                draw.text((34-self.artist_animation_cnt, 7), self.current_artist, self.artist_color, font = self.font)
            
            album_len = self.font.getsize(self.current_album)[0]
            if album_len > 31:
                spacer = "     "
                # draw.text((34-self.album_animation_cnt, 14), self.current_album + spacer + self.current_album, self.album_color, font = self.font)
                self.album_animation_cnt += 1
                if self.album_animation_cnt == self.font.getsize(self.current_album + spacer)[0]:
                    self.album_animation_cnt = 0
            else:
                pass
                # draw.text((34-self.album_animation_cnt, 14), self.current_album, self.album_color, font = self.font)

            draw.rectangle((32,0,33,32), fill=(0,0,0))

            if self.current_art_img is not None:
                frame.paste(self.current_art_img, (0,0))

            drawPlayPause(draw, self.is_playing, self.play_color)

            return frame
        else:

            return None

def drawPlayPause(draw, is_playing, color):
    if not is_playing:
        draw.line((45,22,45,28), fill = color)
        draw.line((46,23,46,27), fill = color)
        draw.line((47,23,47,27), fill = color)
        draw.line((48,24,48,26), fill = color)
        draw.line((49,24,49,26), fill = color)
        draw.line((50,25,50,25), fill = color)
    else:
        draw.line((45,22,45,28), fill = color)
        draw.line((46,22,46,28), fill = color)
        draw.line((49,22,49,28), fill = color)
        draw.line((50,22,50,28), fill = color)

