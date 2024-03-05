import numpy as np
from PIL import Image

def validate(arr):
    # arr[0,0] = [8,4,8] #valid
    # arr[0,0] = [7,4,8] #not valid
    # arr[0,0] = [8,3,8] #not valid
    # arr[0,0] = [8,3,7] #not valid

    return np.all(arr&[2**(8-5)-1, 2**(8-6)-1, 2**(8-5)-1]==[0,0,0]) 


img_names = ['rgb888.png','rgb565_no_dither.png','img_g0_c32_fs0.png','img_g0_c32_fs0.png','img_g0_crgb565_fs0.png','img_g0_crgb565_fs1.png',]
for img_name in img_names:
    img = Image.open(img_name)
    arr = np.array(img)
    valid = validate(arr)
    print(f"image {img_name} is {'valid' if valid else 'INVALID'} RGB565")