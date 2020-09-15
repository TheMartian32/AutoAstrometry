"""
This script has many abilities. Using astroquery it can upload the image to astrometry.net and get a plate solution.
Along with this it can use the SIMBAD service to get coordinates for your target. Then using astropy it can convert
those coordinates to ICRS coordinates. Along with this it can do a lot of other things.
"""

import webbrowser
import time
from astroquery.astrometry_net import AstrometryNet
from astroquery.simbad import Simbad
from rich import print
from rich.table import Table
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
import os


def ask_for(prompt, error_msg=None, _type=None):
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


def redirect_to(url='https://www.google.com'):
    """
    Takes in a URL as a string and asks the user if they would like to be redirected
    to that URL.

    Args:
        url (str, optional): URL that the user needs to be redirected to. Defaults to google.com.
    """
    invalid = True
    while invalid:
        # * Asks the user if they want to be redirect_toed to the website
        print(
            f'\nWould you like to be [bold blue]redirected[/] to: {url} ?')
        redirect_to = ask_for(
            '(y/n): ', error_msg='Wrong data type', _type=str).lower()

        # * If they do want to go to the website it opens it then breaks out of the loop.
        if redirect_to[0] == 'y':
            webbrowser.open_new_tab(f'{url}')
            invalid = False

        # * They don't want to go to the website so it breaks out of the loop.
        elif redirect_to[0] == 'n':
            print('\nContinuing...')
            invalid = False


def simbad_query():
    """
    Looks up target and prints out the information such as RA and Dec.
    When using the function, it automatically asks the user for a target.
    """

    # * Tries to query the target using astroquery if it fails it just opens the SIMBAD website
    try:
        # * Tells user why they need this.
        print(
            '\nTo find the [bold blue]RA and Dec[/] of your target, please put it in here.')
        print("If your target can't be found, it will automatically redirect you to the website to put it in again.")

        # * Asks for target name and tries to look it up then if it can, prints it out.
        target = ask_for('\nTarget name: ')
        query = Simbad.query_object(f'{target}')
        query.pprint()
        # * Asks the user if they wanted to be redirect_toed to the website.
        redirect_to('http://simbad.u-strasbg.fr/simbad/sim-fbasic')
    except:
        # * If theres an error it automatically just opens the website.s
        webbrowser.open('http://simbad.u-strasbg.fr/simbad/sim-fbasic')


def find_fits_dir():
    """
    Gets directory or file of the FITS image.

    Returns:
        File or filepath: Returns the filepath or file of the FITS image.
    """
    look_for = True

    while look_for:
            # * Asks for the directory of the FITS file.
        print('\n-------------------------------------------------------')
        print('What is the path to the image file or directory?')
        print(
            'Please make sure the file [bold blue]ends in .FITS, JPEG, or .PNG[/]')
        print('-------------------------------------------------------')

        time.sleep(2)

        print(
            '\nYou can put in a path for a directory or file. \n(  Directory EX: /Users/user/Pictures | File EX: /Users/user/Pictures/photo.png )')
        print('\nTo [bold blue]copy a file path[/] on Mac right click on file, then hold alt, then select [bold blue]copy as pathname[/].')
        dir_or_file = ask_for('\n: ', _type=str)

        # * Supported file extensions (mainly those just supported by astrometry.net)
        file_extensions = ['.FITS', '.JPEG', '.PNG',
                           '.FIT', '.fits', '.fit', '.fts']

        # * File counter
        counter = 0

        # * Given path is directory
        if os.path.isdir(dir_or_file):
            # * For every file in the directory print out how many there are.
            for file_name in os.listdir(dir_or_file):
                counter += 1
                print(counter)
                print('File: ')
                # * Checks if the file is one of the supported file extensions.
                if file_name.endswith(tuple(file_extensions)):
                    # * Prints out file path
                    print(
                        f'\n{os.path.join(dir_or_file)}/{file_name}')

                    look_for = False
            # * Asks for the image they want to upload.
            print(
                '\nWhich [bold blue]image[/] would you like to [bold blue]upload[/]? (One of the paths above)')
            upload_image = ask_for('\n:')
            return upload_image

        # * Given path is file
        if os.path.isfile(dir_or_file):
            # * Finds out if the file is one of the supported file extensions.
            if dir_or_file.endswith(tuple(file_extensions)):
                # * Prints out path and breaks out of loop.
                print(f'\n{os.path.join(dir_or_file)}')
                look_for = False
                return dir_or_file


def search():
    """
    Using RA and Dec coordinates this function can convert them to
    degrees in the ICRS frame. ( I have zero idea what im talking about )
    """
    search_for_ra_dec = True
    while search_for_ra_dec:

        try:
            # * Uses SkyCoord to convert RA and Dec values to ICRS coordinates
            print(
                '\n[bold blue]Right Ascension[/] and [bold blue]Declination[/] for your target.')
            print(
                'Enter the values [bold]one at a time[/]. ( EX: 19 ( hit enter ), 07 ( hit enter ), 14 ( hit enter )')
            print('The same applies for [bold blue]Declination values[/].')
            ra1 = ask_for('\n: ', _type=int)
            ra2 = ask_for(': ', _type=int)
            ra3 = ask_for(': ', _type=int)

            print("\n[bold blue]Declination[/], don't forget the + or -")
            dec1 = ask_for('\n: ', _type=int)
            dec2 = ask_for(': ', _type=int)
            dec3 = ask_for(': ', _type=int)

            # * Conversion
            c = SkyCoord(f'{ra1}h{ra2}m{ra3}s',
                         f'{dec1}d{dec2}m{dec3}s', frame='icrs', unit='deg')
            print(c)
        # * Value error, user didn't enter in the right values
        except ValueError:
            print('\n[red]Value Error ocurred[/]')
            print('Please [bold blue]re-enter your RA and Dec[/]')
        else:
            # * Got a result so break out of loop
            search_for_ra_dec = False


def upload():
    """
    Using astroquery it asks the user for the
    FITS file then it uploads that file to nova.astronometry.net
    then it solves the image, then redirect_tos the user to the website.
    """

    # * Gets file path for the image to be uploaded
    image = find_fits_dir()

    # * Creating instance of astrometry.net
    ast = AstrometryNet()
    ast.api_key = 'bchkvzadjuswddhg'

    try_again = True
    submission_id = None

    while try_again:
        try:
            if not submission_id:
                # * Solves the image from the file path
                wcs_header = ast.solve_from_image(f'{image}', force_image_upload=True,
                                                  submission_id=submission_id, solve_timeout=1000)
            else:
                # * Time is in seconds.
                wcs_header = ast.monitor_submission(
                    submission_id, solve_timeout=1000)
        except TimeoutError as e:
            # * Timeout error, never triggers. Basically useless code since it never triggers during timeout error
            submission_id = e.args[1]
            print('\nThere was a timeout error. ( Process took to long ).')
            print('Astometry.net could also be down at the moment.')
        else:
            #! got a result, so terminate
            try_again = False

    if wcs_header:
        # * Code to execute when solve succeeds
        print('\nSuccess! :thumbs_up:')
        print(
            '\nTo get the most possible information out of your image please go to the website below.')
        redirect_to('http://nova.astrometry.net/users/20995')

        # * Looks up target with astroquery then can redirect_to user to the website
        # * to use the aladin lite view to find comp stars, look around, etc.
        simbad_query()

        find_icrs_coordinates = ask_for(
            '\nDo you want to find the ICRS position for your target? (y/n): ').lower()

        if find_icrs_coordinates == 'y':
            search()

            convert_comp_stars = True
            while convert_comp_stars:

                # * Asks the user if they have any comparison stars they need the ICRS coordinates for
                print(
                    '\nDo you have any [bold blue]comparison stars[/] that you want to get the [bold blue]ICRS coordinates[/] for? (y/n)')
                comp_stars_icrs = ask_for('\n: ')

                if comp_stars_icrs == 'y':

                    # * Number of comparison stars.
                    print(
                        '\nHow many [bold blue]comparison stars[/] do you have?')
                    num_comp_stars = ask_for(
                        '\n: ', error_msg='Please put in an integer.', _type=int)

                    # * If number of comparison stars is over 10, repeat prompt.
                    if num_comp_stars > 10:
                        print('\nThe limit is 10 comparison stars.')
                    elif num_comp_stars <= 10:
                        for _ in range(num_comp_stars):
                            search()
        elif find_icrs_coordinates == 'n':
            print('\nContinuing...')
            time.sleep(1.25)

        # * redirects to the NASA exoplanet archive
        print(
            '\nThis is to get more information about your target such as the [bold blue]host star[/] information.')
        redirect_to('https://exoplanetarchive.ipac.caltech.edu')
    else:
        #! Code to execute when solve fails
        print('\n[bold red]Failed[/bold red] to solve.')


if __name__ == "__main__":
    print('\n----------------------------------------------------------------------------------')
    print('To use this software please register for an account '
          'on http://nova.astrometry.net')
    print('----------------------------------------------------------------------------------')

    print('\nTo [bold blue]terminate the program[/] press [b]Control+C[/].')
    print(
        '\nIf you get a [bold blue]TIMEOUT ERROR[/], check the link above for your image.')
    time.sleep(1.25)

    print(
        '\n******************** [bold blue]Beginning of program[/] ********************')

    def rerun():
        """
        Loops over the upload method as many times as the user needs.
        """
        # * While the prompt isnt y or n it repeats it
        invalid = True
        while invalid:
            print(
                '\nDo you want to upload [bold blue]more than one file[/]? (y/n)')
            how_many = ask_for(
                '\n: ', 'Error', str).lower()

            if how_many == 'y':
                num_files = ask_for(
                    '\nHow many files do you have that need to be uploaded?: ', 'Not the right data type.', _type=int)
                if num_files > 15:
                    print(
                        'Sorry, the [red]number of files[/red] cannot be over 15.')

                elif num_files <= 15:
                    for _ in range(num_files):
                        # * For every file the user needs to upload, it calls the upload function.
                        upload()
                        invalid = False

            elif how_many == 'n':
                # * Uploads only one file.
                upload()
                invalid = False

    rerun()

    print('\nDo you have any [bold blue]more images[/] to be uploaded? '
          '(y/n)')
    repeat = ask_for('\n: ', 'Error', str).lower()

    if repeat == 'y':
        upload()
        rerun()
    if repeat == 'n':
        print('\n********************'
              ' [bold blue]End of program[/] '
              '********************')
