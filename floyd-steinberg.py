# based on https://scipython.com/blog/floyd-steinberg-dithering/
import numpy as np
from PIL import Image

def get_new_val(old_val, nc):
    """
    Get the "closest" colour to old_val in the range [0,1] per channel divided
    into nc values.

    """

    if nc == 'rgb565':
        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        new_val = np.empty_like(old_val)

        # https://stackoverflow.com/questions/12116830/numpy-slice-of-arbitrary-dimensions

        # limit g to 62 to give g the same brightness range as r and b, this preserves pure white colors and simplifies calculation
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
# TODO: fix this code and optimize it (searching full space is too costly with many colors, so only calculate subset of color space around rounded color value (-1,+0,+1 for all 3 colors? for a total of 27 colors to search?))
    
def color_range_max(nc):
    if nc == 'rgb565':
        # limit g to 62 to give g the same brightness range as r and b, this preserves pure white colors and simplifies calculation
        max = 248
    else:
        max = (nc-1)*(256/nc)
    return max

def fs_dither(img, nc):
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr = np.array(img, dtype=np.single) / 255
    
    IMG_HEIGHT = arr.shape[0]
    IMG_WIDTH  = arr.shape[1]

    for ir in range(IMG_HEIGHT):
        for ic in range(IMG_WIDTH):
            old_val = arr[ir, ic].copy() # copy to prevent overwriting old_val when writing to arr
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

    # carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8) # increase dynamic range if possible, then map to 0-255 (may not be integer multiple)
    # carr = np.array(arr * 255, dtype=np.uint8) # map to 0-255 (may not be integer multiple of nc)                            
    carr = np.array(arr * color_range_max(nc), dtype=np.uint8) # map to 0-max_of_nc (is always integer multiple of nc)   

    return Image.fromarray(carr)


def palette_reduce(img, nc):
    """Simple palette reduction without dithering."""
    arr = np.array(img, dtype=np.single) / 255

    # # increase dynamic range:
    # arr = np.clip(arr * 2 - 0.10, 0, 1)

    arr = get_new_val(arr, nc)

    max = color_range_max(nc)

    carr = np.array(arr * max, dtype=np.uint8)
    return Image.fromarray(carr)


if __name__ == "__main__":
    img_name = 'rgb888.png'
    #img_name = '1665_girl_with_a_pearl_earring_sm.jpg'

    img = Image.open(img_name)

    # # convert to greyscale
    # img = img.convert('L')
    # greyscale = True # g1

    # for nc in (2,3,4):
    for nc in (2,3,4,8,32,'rgb565',):
    # for nc in ('rgb565',):
        print(f'number of colors = {nc}')
        dim = fs_dither(img, nc)
        dim.save('img_g0_c{}_fs1.png'.format(nc))
        rim = palette_reduce(img, nc)
        rim.save('img_g0_c{}_fs0.png'.format(nc))