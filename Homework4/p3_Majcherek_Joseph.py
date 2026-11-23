"""
Problem 3: Fade to Black and White Animation
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def image_load(filename):
    """Load an image file into an ndarray."""
    return plt.imread(filename)


def convert_bw(img):
    """
    Part a: Convert an ( H, W, 3) uint8 RGB image to an (H, W, 3) uints greyscale
    image using vectorized NumPy operations (no loops).
    """
    # Compute average across the 3 color channels (axis=2) and cast back to uint8
    grey_2d = np.mean(img, axis=2).astype(np.uint8)
    # Stack along the 3rd dimension so each pixel is [avg, avg, avg]
    bw_img = np.dstack((grey_2d, grey_2d, grey_2d))
    return bw_img



def image_gen(filename, steps=30):
    """
    Part b: Generator yielding intermediate frames transitioning from the 
    original color image to its B/W version and back.
    """
    img1 = image_load(filename)
    img2 = convert_bw(img1)

    # s varies from 0.0 (color) to 1.0 (B/W) and back to 0.0 (color)
    svalues = np.hstack([np.linspace(0.0, 1.0, steps), np.linspace(1.0, 0.0, steps)])

    # Pre-compute transition frames
    images = [np.uint8(img1 * (1.0 - s) + img2 * s) for s in svalues]

    while True:
        for img in images:
            yield img


# Part c: Set up figure and run animation from terminal
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_filename = os.path.join(BASE_DIR, "Grand_Teton-800-480.jpg")
fig = plt.figure()
im = plt.imshow(image_load(img_filename), interpolation="none", animated=True)

imggen = image_gen(img_filename, steps=30)


def updatefig(*args):
    global imggen
    img_array = next(imggen)
    im.set_array(img_array)
    return (im,)


ani = animation.FuncAnimation(fig, updatefig, interval=60, blit=False)
plt.title("Image transformation to B/W")
plt.show()