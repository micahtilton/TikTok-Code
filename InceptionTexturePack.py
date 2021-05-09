from PIL import Image
from functools import reduce, lru_cache
from glob import glob

TEXTURE_PACK_SIZE = 16

def add_color(pixel_one, pixel_two):
    ret = []
    for one, two in zip(pixel_one, pixel_two):
        ret.append(one + two)
    return ret

def average_color(pixels):
    average = []
    for color in reduce(add_color, pixels):
        average.append(color // len(pixels))
    return tuple(average)    

image_averages = dict()
def get_valid_images():
    global image_averages

    for img_path in glob(r"Inception - Copy\assets\minecraft\textures\block\*.png", recursive=True):
        pixels = []
        valid = True
        count = 0
        for pixel in Image.open(img_path).convert('RGBA').getdata():
            count += 1
            if pixel[-1] != 255 or count > 256:
                valid = False
                break
            else:
                pixels.append(pixel)
        if valid and count == 256:
            image_averages[average_color(pixels)] = img_path
get_valid_images()

def color_difference(color_one, color_two):
    ret = 0
    for one, two in zip(color_one, color_two):
        ret += abs(one - two)
    return ret

@lru_cache(maxsize=16)
def path_to_closest_color(color):
    global image_averages
    min_dif = float('inf')
    ret_color = None
    for color_check in image_averages.keys():
        dif = color_difference(color, color_check)
        if dif < min_dif:
            ret_color = color_check
            min_dif = dif
    return image_averages[ret_color]

def change_images():
    for img_path in glob(r"Inception - Copy\assets\minecraft\**\*.png", recursive=True):
        new_path = img_path.replace('Inception - Copy', 'Inception')
        change_image = Image.open(img_path).convert('RGBA')
        width, height = change_image.size
        new_img = Image.new("RGBA", (width*TEXTURE_PACK_SIZE, height*TEXTURE_PACK_SIZE), color=(0,0,0,0))
        for i, pixel in enumerate(change_image.getdata()):
            y, x = divmod(i, width)
            x *= TEXTURE_PACK_SIZE
            y *= TEXTURE_PACK_SIZE
            alpha = pixel[-1]

            if alpha == 0:
                continue

            add_img = path_to_closest_color(pixel)
            for j, new_pixel in enumerate(Image.open(add_img).convert("RGBA").getdata()):
                new_pixel = list(new_pixel)
                new_pixel[-1] = alpha
                ny, nx = divmod(j, TEXTURE_PACK_SIZE)
                new_img.putpixel((nx+x, ny+y), tuple(new_pixel))
        new_img.save(new_path)
        print(new_path)
change_images()