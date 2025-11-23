# Reverse Fisheye in Python
A simple reverse fisheye dewarping program made in Python, with one implementation using cv2 and numpy, and the other using just math.

Example input images are given as fisheye.png/ppm that I used from here: https://www.reddit.com/r/blenderhelp/comments/zwux8m/how_to_invert_fisheye_lens/

revfish.py: is a more traditional implementation, by using cv2 and numpy, but there's much to be desired as it fully inverts the fisheye, leading to an inverted, panorama-like look that stretches as it approaches the ends instead of compressing.

mathrevfish.py: is a mathematical way of doing this without any libraries, but does require a bit more finessing of constants and zoom out factors to get a desired, flat output. And even when it does, it still needs to crop the edges to avoid the same stretched look. Also, you should use .ppm image files for this program.

Ultimately, the best method would be to use a dedicated program with after effects or some other kind of photoshop, but if you don't have that, this is a pretty good example of what you can do with a bit of code and math.
