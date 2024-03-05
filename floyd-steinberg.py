# based on https://scipython.com/blog/floyd-steinberg-dithering/
import numpy as np
from PIL import Image

# GREYSCALE = False

# img_name = '1665_Girl_with_a_Pearl_Earring.jpg'
# img_small_name = '1665_girl_with_a_pearl_earring_sm.jpg'
# IMG_HEIGHT = 473
# IMG_WIDTH = 400


# try:
#     img = Image.open(img_small_name)
#     if GREYSCALE:
#         img = img.convert('L')
# except:
#     img = Image.open(img_name)
#     if GREYSCALE:
#         img = img.convert('L')

#     width, height = img.size
#     new_width = IMG_WIDTH
#     new_height = int(height * new_width / width)
#     img = img.resize((new_width, new_height))
#     #img = img.resize((new_width, new_height), Image.ANTIALIAS) #module 'PIL.Image' has no attribute 'ANTIALIAS'
#     img.save(img_small_name)


img_name = 'rgb888.png'
IMG_HEIGHT = 256
IMG_WIDTH = 256
img = Image.open(img_name)

# p = []
# for r in range(32):
#     for g in range(64):
#         for b in range(32):
#             # p.append([r*2/7,g/7,b*2/7])
#             p.append([r*2/63,g/63,b*2/63])


def get_new_val(old_val, nc):
    """
    Get the "closest" colour to old_val in the range [0,1] per channel divided
    into nc values.

    """

    if nc == 'rgb565':
        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        new_val = np.empty_like(old_val)

        # https://stackoverflow.com/questions/12116830/numpy-slice-of-arbitrary-dimensions

        # limit g to 62 to give g the same brightness range as r and b
        new_val[...,0] = np.round(old_val[...,0] * (31))*2 / 62
        new_val[...,1] = np.round(old_val[...,1] * (62))   / 62   
        new_val[...,2] = np.round(old_val[...,2] * (31))*2 / 62
        
        return new_val

    else:
        return np.round(old_val * (nc - 1)) / (nc - 1)


#For RGB images, the following might give better colour-matching.
# p = np.linspace(0, 1, nc)
# p = np.array(list(product(p,p,p)))
# def get_new_val(old_val):
#    idx = np.argmin(np.sum((old_val[None,:] - p)**2, axis=1))
#    return p[idx]
    
def color_range_max(nc):
    if nc == 'rgb565':
        # limit g to 62 to give g the same brightness range as r and b
        max = 248
    else:
        max = (nc-1)*(256/nc)
    return max

def fs_dither(img, nc):
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr_raw = np.array(img, dtype=np.single)
    arr = np.array(img, dtype=np.single) / 255
    

    for ir in range(IMG_HEIGHT):
        for ic in range(IMG_WIDTH):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_val = arr[ir, ic].copy()
            new_val = get_new_val(old_val, nc)
            arr[ir, ic] = new_val
            err = old_val - new_val
            # In this simple example, we will just ignore the border pixels.
            if ic < IMG_WIDTH - 1:
                arr[ir, ic+1] += err * 7/16
            if ir < IMG_HEIGHT - 1:
                if ic > 0:
                    arr[ir+1, ic-1] += err * 3/16
                arr[ir+1, ic] += err * 5/16
                if ic < IMG_WIDTH - 1:
                    arr[ir+1, ic+1] += err / 16

    # carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8) # if possible increase dynamic range, then map to 0-255 (may not be integer multuple)
    # carr = np.array(arr * 255, dtype=np.uint8) # map to 0-255 (may not be integer multuple)
                    
    max = color_range_max(nc) # map to 0-max (is always integer multiple of nc)
                            
    carr = np.array(arr * max, dtype=np.uint8)

    # print(carr[0,0:20,:])
    # print(carr[64,0:20,:])
    return Image.fromarray(carr)


def palette_reduce(img, nc):
    """Simple palette reduction without dithering."""
    arr = np.array(img, dtype=np.single) / 255
    arr = get_new_val(arr, nc)

    max = max = color_range_max(nc)

    carr = np.array(arr/np.max(arr) * max, dtype=np.uint8)
    return Image.fromarray(carr)

# rim = palette_reduce(img, 'rgb565')
# rim.save('rimg-{}.png'.format('rgb565'))

# for nc in (32,):
# for nc in (2, 3, 4, 8, 16, 32):
for nc in ('rgb565',): # (2, 3, 4, 8, 16):
    print('nc =', nc)
    dim = fs_dither(img, nc)
    dim.save('img_{}_dither.png'.format(nc))
    rim = palette_reduce(img, nc)
    rim.save('img_{}_no_dither.png'.format(nc))


