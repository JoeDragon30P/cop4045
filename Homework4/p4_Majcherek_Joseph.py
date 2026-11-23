"""
Problem 4: Miniature (Tilt-Shift) Effect
"""

import os
import numpy as np
from image_blur import image_load, image_save, img_blur


def img_miniature(img, kernel_sizes=None, focus_slice=6):
    """
    Part a: Apply a miniature tilt-shift effect by splitting the image into
    horizontal slices and blurring slices outside the focal band using
    img_blur() from image_blur.py.
    """
    if kernel_sizes is None:
        # 12 horizontal zones: strong blur at top/bottom, sharp focus in the middle
        kernel_sizes = [25, 21, 17, 13, 9, 5, 1, 1, 5, 11, 17, 23]

    num_slices = len(kernel_sizes)
    h, w, _ = img.shape
    slice_h = h // num_slices
    result = img.copy()

    for idx, k_size in enumerate(kernel_sizes):
        r0 = idx * slice_h
        r1 = h if idx == num_slices - 1 else (idx + 1) * slice_h

        # Leave the sharp focal slice(s) unblurred
        if k_size <= 1 or idx == focus_slice:
            continue

        # Include vertical overlap padding so slice edges blend smoothly without dark borders
        pad = k_size // 2
        pad_r0 = max(0, r0 - pad)
        pad_r1 = min(h, r1 + pad)

        weights = np.ones((k_size, k_size))
        blurred_region = img_blur(img[pad_r0:pad_r1, :], weights)

        # Copy the non-padded portion back into the output image
        trim_top = r0 - pad_r0
        trim_bot = trim_top + (r1 - r0)
        result[r0:r1, :] = blurred_region[trim_top:trim_bot, :]

    return result


def main():
    """Part b: Load photo, apply miniature effect, and save output image."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "Grand_Teton-800-480.jpg")
    output_file = os.path.join(base_dir, "Grand_Teton-800-480-miniature.png")

    orig_img = image_load(input_file)
    mini_img = img_miniature(orig_img)
    image_save(output_file, mini_img)
    print(f"Miniature effect saved to {output_file}")


if __name__ == "__main__":
    main()