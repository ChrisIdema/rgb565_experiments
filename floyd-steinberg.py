#https://scipython.com/blog/floyd-steinberg-dithering/
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
        new_val = old_val
        #works for reducing bitdepth:
        # new_val[:,:,0] = np.round(old_val[:,:,0] * (32 - 1)*2) / (64 - 1)
        # new_val[:,:,1] = np.round(old_val[:,:,1] * (64 - 1))   / (64 - 1)
        # new_val[:,:,2] = np.round(old_val[:,:,2] * (32 - 1)*2) / (64 - 1)

        # todo check math
        new_val[0] = np.round(old_val[0] * (32 - 1))*2 / (64 - 1)
        new_val[1] = np.round(old_val[1] * (64 - 1))   / (64 - 1)
        new_val[2] = np.round(old_val[2] * (32 - 1))*2 / (64 - 1)

        return new_val

    else:
        # return np.round(old_val * (nc - 1)) / (nc - 1)

        # p = np.linspace(0, 1, nc)    
        # p = np.array(list(np.product(p,p,p)))



        p = []
        for r in range(4):
            for g in range(8):
                for b in range(4):
                    p.append([r*2/7,g/7,b*2/7])

        # print(p)

        #p = np.array([[1,1,1],[0.5,0.5,0.5],[0,0,0],[1,0,0]])

        idx = np.argmin(np.sum((old_val - p)**2, axis=1))
        return p[idx]

#For RGB images, the following might give better colour-matching.
# p = np.linspace(0, 1, nc)
# p = np.array(list(product(p,p,p)))
# def get_new_val(old_val):
#    idx = np.argmin(np.sum((old_val[None,:] - p)**2, axis=1))
#    return p[idx]

def fs_dither(img, nc):
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr = np.array(img, dtype=float) / 255

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

    # carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8)
    carr = np.array(arr * 255, dtype=np.uint8)
    return Image.fromarray(carr)


def palette_reduce(img, nc):
    """Simple palette reduction without dithering."""
    arr = np.array(img, dtype=float) / 255
    arr = get_new_val(arr, nc)

    carr = np.array(arr/np.max(arr) * 255, dtype=np.uint8)
    return Image.fromarray(carr)

# rim = palette_reduce(img, 'rgb565')
# rim.save('rimg-{}.png'.format('rgb565'))

# for nc in (32,):
# for nc in (2, 3, 4, 8, 16, 32):
for nc in ('rgb565',): # (2, 3, 4, 8, 16):
    print('nc =', nc)
    dim = fs_dither(img, nc)
    dim.save('dimg-{}.png'.format(nc))
    #rim = palette_reduce(img, nc)
    #rim.save('rimg-{}.png'.format(nc))
