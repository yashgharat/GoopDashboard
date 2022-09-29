import sys
import random
from json import load
from PIL import Image
from time import sleep

class GoopScreen():
    def __init__(self, color="green", path="../assets/sprite/"):
        self.color = color
        self.path = path
        self.anim_frame = 0
        self.cur_anim = []
        self.goop_dict = self.load_goop()
    
    def generate(self):
        frame = None
        # Get the current animation based on AI or random if not mid animation
        if(self.anim_frame >= len(self.cur_anim)):
            self.anim_frame = 0
            rand_key = random.choice(['jump', 'walk', 'idle']) #[list(self.goop_dict)])
            self.cur_anim = self.goop_dict['walk']

        frame = self.cur_anim[self.anim_frame].convert("RGB")
        print(self.anim_frame, len(self.cur_anim))
        self.anim_frame = self.anim_frame + 1
        
        return frame

    
    def load_goop(self):
        sheet = Image.open(self.path+self.color+".png")
        width, height = sheet.size
        anim_sprites = []
        anim_keys = ['jump', 'walk', 'idle', 'dash', 'hurt', 'death']

        for y in range(0, height, 16):
            cur_anim = []
            for x in range(0, width, 16):
                sprite = sheet.crop((x, y, x+16, y+16))
                if sprite.getbbox() is not None:
                    cur_anim.append(sprite)
            anim_sprites.append(cur_anim)
        
        return dict(zip(anim_keys, anim_sprites))