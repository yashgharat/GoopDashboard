import sys
from PIL import Image
from time import sleep
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def main():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.brightness = 50
    options.gpio_slowdown = 2
    options.pwm_lsb_nanoseconds = 80
    options.limit_refresh_rate_hz = 150
    options.drop_privileges=False

    matrix = RGBMatrix(options = options)

    sheet = load_sprite_sheet()
    num_anims = len(sheet)
    try:
        print("Press CTRL-C to stop.")
        while True:
            # for x in range(num_anims):
            for y in range(len(sheet[2])):
                frame = sheet[2][y].convert("RGB").copy()
                matrix.SetImage(frame)
                sleep(0.1)
                # sleep(1)
    except KeyboardInterrupt:
        sys.exit(0) 


def load_sprite_sheet(color:str="green"):
    sheet = Image.open("../assets/sprite/"+color+".png")
    width, height = sheet.size
    cnt = 1
    sprite_anims = []

    for y in range(0, height, 16):
        cur_anim = []
        for x in range(0, width, 16):
            sprite = sheet.crop((x, y, x+16, y+16))
            if sprite.getbbox() is not None:
                # sprite.save("../assets/sprite/temp/image_"+str(cnt)+".png")
                cur_anim.append(sprite)
            # sleep(1)
            cnt=cnt+1
        sprite_anims.append(cur_anim)
    return sprite_anims

main()