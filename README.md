# rgb565_experiments

https://en.wikipedia.org/wiki/List_of_monochrome_and_RGB_color_formats#16-bit_RGB_(also_known_as_RGB565)

https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

```
<svg height="300" width="512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" x2="100%" y1="0%" y2="0%">
      <stop offset="0%" stop-color="#FF0000"/>
      <stop offset="100%" stop-color="black"/>
    </linearGradient>
    <linearGradient id="grad2" x1="0%" x2="100%" y1="0%" y2="0%">
      <stop offset="0%" stop-color="#00FF00"/>
      <stop offset="100%" stop-color="black"/>
    </linearGradient>
    <linearGradient id="grad3" x1="0%" x2="100%" y1="0%" y2="0%">
      <stop offset="0%" stop-color="#0000FF"/>
      <stop offset="100%" stop-color="black"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0"   width="512" height="100" fill="url(#grad1)"/>
  <rect x="0" y="100" width="512" height="100" fill="url(#grad2)"/>
  <rect x="0" y="200" width="512" height="100" fill="url(#grad3)"/>
</svg>
```


https://inkscape.org/~doctormo/%E2%98%85art-png-export

raster_output_artex.py
```
<dependency type="executable" location="path">optipng</dependency>
```
https://gist.github.com/hidsh/7065820

https://www.geeksforgeeks.org/create-transparent-png-image-with-python-pillow/
v
https://scipython.com/blog/floyd-steinberg-dithering/

colorbanding in rgb565 is worse than in rgb555 since white color lookse worse as some pixels are more green and others more purple
one workaround could give change in color(ratio between colors) a higher penalty than change in brightness
changing color format to HSV might be useful for this
get closed color in terms of Hue and saturation and give lightness error a lower weight and maybe only use lightness for dither?
or give green a higher weigth

https://en.wikipedia.org/wiki/HSL_and_HSV
https://math.hws.edu/graphicsbook/demos/c2/rgb-hsv.html
