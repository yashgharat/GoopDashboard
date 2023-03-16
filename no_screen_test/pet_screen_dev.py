import sys
import random
from json import load
from PIL import Image
from time import sleep

class PetScreen():
    def __init__(self, path="../assets/sprite/"):
        self.path = path
        self.anim_frame = 0
        self.cur_anim = []
        # self.goop_dict = self.load_goop()
        self.anim_dict = self.load_shroom()
    
    def generate(self):
        frame = None
        # Get the current animation based on AI or random if not mid animation
        if(self.anim_frame >= len(self.cur_anim)):
            self.anim_frame = 0
            rand_key = random.choice(list(self.anim_dict.keys())) #['jump', 'walk', 'idle'])
            self.cur_anim = self.anim_dict['hurt']

        frame = self.cur_anim[self.anim_frame].convert("RGB")
        # print(self.anim_frame, len(self.cur_anim))
        self.anim_frame = self.anim_frame + 1
        
        return frame

    
    def load_goop(self, color='green'):
        sheet = Image.open(self.path+'slime_goop/'+color+".png")
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
    
    def load_shroom(self):
        sheet = Image.open(self.path+'mushroom/'+'Mushroom.png')
        width, height = sheet.size
        anim_sprites = []
        uncut = []
        anim_keys = ['idle', 'jump', 'attack', 'hurt', 'death']

        # sheet is only 32 px tall
        for x in range (0, width, 32):
            sprite = sheet.crop((x, 0, x+32, 32))
            if sprite.getbbox() is not None:
                uncut.append(sprite)
        
        # Manual Work for now (optimize later?)
        anim_sprites.append(uncut[0:4])
        anim_sprites.append(uncut[4:15])
        anim_sprites.append(uncut[15:20])
        anim_sprites.append(uncut[20:24])
        anim_sprites.append(uncut[24:])

        return dict(zip(anim_keys, anim_sprites))
        

                    