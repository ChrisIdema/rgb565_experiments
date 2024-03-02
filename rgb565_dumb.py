
from PIL import Image 

#https://www.geeksforgeeks.org/create-transparent-png-image-with-python-pillow/
  
img = Image.open('drawing.png') 
rgba = img.convert("RGBA") 
datas = rgba.getdata() 
  
newData = [] 
for item in datas: 

    r,g,b,a = item[0], item[1], item[2], item[3]

    r = round(r*(31.0/255.0))*8
    g = round(g*(63.0/255.0))*4
    b = round(b*(31.0/255.0))*8

    newData.append((r, g, b, a)) 


rgba.putdata(newData) 
rgba.save("drawing2.png", "PNG") 