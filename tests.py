from astroquery.astrometry_net import AstrometryNet
from rich import print
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
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


def search():
    from astropy.coordinates import SkyCoord
    from astropy import units as u

    ra1 = ask_for('\n: ', _type=int)
    ra2 = ask_for('\n: ', _type=int)
    ra3 = ask_for('\n: ', _type=int)

    dec1 = ask_for('\n: ', _type=int)
    dec2 = ask_for('\n: ', _type=int)
    dec3 = ask_for('\n: ', _type=int)

    c = SkyCoord(f'{ra1}h{ra2}m{ra3}s',
                 f'{dec1}d{dec2}m{dec3}s', frame='icrs', unit='deg')

    print(c)
