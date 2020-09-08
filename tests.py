from rich import print
from astropy.io import fits
"""
A module dedicated purely for testing out new features.
9 / 7 / 20
"""


def ask_for(prompt, error_msg=None, _type=None, delay=0):
    """ While the desired prompt is not given, it repeats the prompt. """
    while True:
        inp = input(prompt).strip()
        if not inp:
            if error_msg:
                print(error_msg)
            continue

        if _type:
            try:
                inp = _type(inp)
            except ValueError:
                if error_msg:
                    print(error_msg)
                continue

        return inp


def search(image_path):

    image = fits.open(image_path)
    data = image[1].data

    # * Getting the Right Ascension and Declination for the center of the image
    center_ra = ask_for(
        '\nWhat is the RA (Right Ascension) of the center of the image?: ')
    center_dec = ask_for(
        'What is the declination of the center of the image?: ')

    # * Getting the target Right Ascension and Declination in degrees
    target_ra = ask_for('\nWhat is the RA of your target in degrees?: ')
    target_dec = ask_for(
        'What is the declination of your target in degrees?: ')

    pixel_scale = ask_for(
        '\nWhat is the pixel scale of your image? ( unit/pixel ): ')

    H, W = image.shape

    x = int((target_ra-center_ra) / pixel_scale + W / 2)
    y = int((target_dec-center_dec) / pixel_scale + H / 2)

    patch_size = 50
    image_patch = image[x - patch_size:x +
                        patch_size, y - patch_size: y+patch_size]
    return image_patch
