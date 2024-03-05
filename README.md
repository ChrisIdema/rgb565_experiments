# rgb565_experiments

This project has modified a dithering example to support rgb565 among some other changes.
It is based on this project: https://scipython.com/blog/floyd-steinberg-dithering/

Colorbanding in gradients in rgb565 is worse than in rgb555 since white color looks worse as some pixels are more green and others more purple instead of just color banding in shades of grey.
Using Floyd-Steinberg dithering will reduce colorbanding by compensating for color error of pixels in neighboring pixels.

Since not every color component has the same number of bits they have to be treated seperately when finding the closest possible value (get_new_val). 
This proved to be worth it since it produces better results for both green and white gradients compared to rgb555. This shows that giving green 1 more bit was a good design choice in rgb565 since our eyes are more sensitive to green.

Another problem with rgb565 if it is implemented as masked bits in rgb888 is that green will have a greater range compared to red and blue of 252 instead of 248 (equivalent of 31.5 vs 31.0).
This can shift the ratio between r,g and b or lead to clipping.
In this implementation I've limited the range of green to 248, this gives green the same range as r and b and will be a superset (all values of r and b plus all values in between).

In this implementation I will only use integer scaling to convert the values to 24-bit color. This reduces the maximum brightness for some palettes, but it prevents introducing new rounding errors. One way to somewhat compensate for this is to normalize the source image somewhat before applying dither if it pretty dark.
Normalization is also called histogram/constrast stretching/equalization. Normalization can also significantly reduce quantization error if image is very low contrast.

The output format is lossless png and colors are saved as rgb888. In order to convert it to binary you would need to convert/map the colors to the right bitformat (should be either integer division and bit shifting or mapping the colors to a palette index)


# Links
- https://en.wikipedia.org/wiki/List_of_monochrome_and_RGB_color_formats#16-bit_RGB_(also_known_as_RGB565)
- https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
- https://scipython.com/blog/floyd-steinberg-dithering/
- https://www.geeksforgeeks.org/create-transparent-png-image-with-python-pillow/
- https://en.wikipedia.org/wiki/Normalization_(image_processing)
- https://en.wikipedia.org/wiki/HSL_and_HSV
- https://math.hws.edu/graphicsbook/demos/c2/rgb-hsv.html


# Todo
* modify function so that dither function only works with np-arrays and not with PIL images so it is not dependend on PIL and adding more pre-/postprocesing would be cleaner
* add command line parameters(greyscale conversion (float), dynamic range, different cost function, integer scale or float scale etc.)
* greyscale in rgb mode (should be easy, just calculate average rgb value in float and put those values in r,g and b)
* support for 7-colour Waveshare e-paper or Pimoroni e-ink 
* test transparency
* test if cost function works better if image is in HSV mode
* Gimp plugin
* inkscape plugin
* C/C++ version (maybe even constexpr)

