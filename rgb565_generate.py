from PIL import Image 
import numpy as np

w=256
h=256
a = np.zeros((h,w,3))

a[64*0:64*1,:,0] = np.arange(256)
a[64*1:64*2,:,1] = np.arange(256)
a[64*2:64*3,:,2] = np.arange(256)
a[64*3:64*4,:,:] = a[64*0,:,:] + a[64*1,:,:] + a[64*2,:,:]

img = Image.fromarray(np.uint8(a))
img.save("rgb888.png", "PNG") 


# a[:,:,0] = np.uint8(a[:,:,0]*(31.0/255.0))*8
# a[:,:,1] = np.uint8(a[:,:,1]*(63.0/255.0))*4
# a[:,:,2] = np.uint8(a[:,:,2]*(31.0/255.0))*8

# limit g to 62 to give g the same brightness range as r and b (superset of r and b possible values)
a[:,:,0] = np.round(a[:,:,0]/255 * (31))*8
a[:,:,1] = np.round(a[:,:,1]/255 * (62))*4   
a[:,:,2] = np.round(a[:,:,2]/255 * (31))*8

# print(a[200,:,:])
img = Image.fromarray(np.uint8(a))
img.save("rgb565_no_dither.png", "PNG") 
