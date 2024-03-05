import numpy as np
from PIL import Image

img_name = 'rgb888.png'

img_name = 'rgb565_no_dither.png'

def validate(arr):
    # arr[0,0] = [8,4,8] #valid
    # arr[0,0] = [7,4,8] #not valid
    # arr[0,0] = [8,3,8] #not valid
    # arr[0,0] = [8,3,7] #not valid

    return np.all(arr&[2**(8-5)-1, 2**(8-6)-1, 2**(8-5)-1]==[0,0,0]) 


img_names = ['rgb888.png','rgb565_no_dither.png','img_32_no_dither.png','img_32_dither.png','img_rgb565_no_dither.png','img_rgb565_dither.png',]

for img_name in img_names:
    img = Image.open(img_name)
    arr = np.array(img)
    valid = validate(arr)
    print(f"image {img_name} is {'valid' if valid else 'INVALID'} RGB565")