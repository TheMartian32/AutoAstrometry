import webbrowser
import time
from astroquery.astrometry_net import AstrometryNet
from rich import print
from rich.table import Table
from astroquery.simbad import Simbad
from astropy.io import fits
import os


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


def redirect(url='https://www.google.com'):
    """
    Takes in a URL as a string and asks the user if they would like to be redirected
    to that URL.

    Args:
        url (str, optional): URL that the user needs to be redirected to. Defaults to str.
    """
    invalid = True
    while invalid:
        # * Asks the user if they want to be redirected to the website
        print(f'\nWould you like to be [blue]redirected[/blue] to: {url} ?')
        redirect = ask_for(
            '(y/n): ', error_msg='Wrong data type', _type=str).lower()

        # * If they do want to go to the website it opens it then breaks out of the loop.
        if redirect[0] == 'y':
            webbrowser.open_new_tab(f'{url}')
            invalid = False

        # * They don't want to go to the website so it breaks out of the loop.
        elif redirect[0] == 'n':
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
            '\nTo find the [blue]RA and Dec[/blue] of your target, please put it in here.')
        print("If your target can't be found, it will automatically redirect you to the website to put it in again.")

        # * Asks for target name and tries to look it up then if it can, prints it out.
        target = ask_for('\nTarget name: ')
        query = Simbad.query_object(f'{target}')
        query.pprint()
        # * Asks the user if they wanted to be redirected to the website.
        redirect('http://simbad.u-strasbg.fr/simbad/sim-fbasic')
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
        print('What is the path to the FITS file or directory?')
        print(
            'Please make sure the file [bold blue]ends in .FITS, JPEG, or .PNG[/bold blue]')
        print('-------------------------------------------------------')

        print(
            '\nYou can put in a path for a directory or file. \n(  Directory EX: /Users/user/Pictures | File EX: /Users/user/Pictures/photo.png )')
        print('\nTo [bold blue]copy a file path[/] on Mac right click on file, then hold alt, then select [bold blue]copy as pathname[/].')
        dir_or_file = ask_for('\n: ', _type=str)

        file_extensions = ['.FITS', '.JPEG', '.PNG',
                           '.FIT', '.fits', '.fit', '.fts']

        # * File counter
        counter = 0

        # * Given path is directory
        if os.path.isdir(dir_or_file):
            for file_name in os.listdir(dir_or_file):
                counter += 1
                print(counter)
                if file_name.endswith(tuple(file_extensions)):
                    print(
                        f'File: {os.path.join(dir_or_file)}/{file_name}')

                    look_for = False

        # * Given path is file
        if os.path.isfile(dir_or_file):
            if dir_or_file.endswith(tuple(file_extensions)):
                print(f'\nFile: {os.path.join(dir_or_file)}')
                look_for = False
                return dir_or_file


def upload(self):
    """
    Using astroquery it asks the user for the
    FITS file then it uploads that file to nova.astronometry.net
    then it solves the image, then redirects the user to the website.
    """

    fits_file = ask_for(
        '\nPlease provide a path to the file you would like to upload: ')

    # * Creating instance of astrometry.net
    ast = AstrometryNet()
    ast.api_key = 'bchkvzadjuswddhg'

    try_again = True
    submission_id = None

    while try_again:
        try:
            if not submission_id:
                # * Solves the image from the file path
                wcs_header = ast.solve_from_image(f'{fits_file}',
                                                  submission_id=submission_id)
            else:
                # * Time is in seconds.
                wcs_header = ast.monitor_submission(submission_id,
                                                    solve_timeout=1500)
        except TimeoutError as e:
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
        redirect('http://nova.astrometry.net/users/20995')

        # * Looks up target with astroquery then can redirect user to the website
        # * to use the aladin lite view to find comp stars, look around, etc.
        simbad_query()

        # * Redirects to the NASA exoplanet archive
        print(
            '\nThis is to get more information about your target such as the [blue]host star[/blue] information.')
        redirect('https://exoplanetarchive.ipac.caltech.edu')
    else:
        #! Code to execute when solve fails
        print('\n[bold red]Failed[/bold red] to solve.')

# def search(self, image):
#     """
#     In progress not ready for use yet
#     Note: Use JS9 API.

#     Args:
#         image (FITS): FITS image.

#     Returns:
#         Float: Returns pixel values in the form of a floating point number
#     """
#     fits_image = image

#     # * Uses filepath
#     hdul = fits.open(fits_image)
#     hdr = hdul[0].header
#     print(list(hdr.keys()))

#     # * Getting the Right Ascension and Declination for the center of the image
#     center_ra = ask_for(
#         '\nWhat is the RA (Right Ascension) of the center of the image?: ')
#     center_dec = ask_for(
#         'What is the declination of the center of the image?: ')

#     # * Getting the target Right Ascension and Declination in degrees
#     target_ra = ask_for('\nWhat is the RA of your target in degrees?: ')
#     target_dec = ask_for(
#         'What is the declination of your target in degrees?: ')

#     pixel_scale = ask_for(
#         '\nWhat is the pixel scale of your image? ( unit/pixel ): ')

#     H, W = search_through.shape

#     x = int((target_ra-center_ra) / pixel_scale + W / 2)
#     y = int((target_dec-center_dec) / pixel_scale + H / 2)

#     patch_size = 50
#     image_patch = search_through[x - patch_size:x +
#                                  patch_size, y - patch_size: y+patch_size]
#     return image_patch


if __name__ == "__main__":
    print('\n----------------------------------------------------------------------------------')
    print('To use this software please register for an account '
          'on http://nova.astrometry.net')
    print('----------------------------------------------------------------------------------')

    print('\nTo [red]terminate the program[/] press [b]Control+C[/].')
    time.sleep(1.25)

    print(
        '\n******************** [blue]Beginning of program[/] ********************')

    print('\nThis is the autofind branch. Remove and merge branches when done.')

    find_fits_dir()

    def rerun():
        """
        Loops over the upload method as many times as the user needs.
        """
        # * While the prompt isnt y or n it repeats it
        invalid = True
        while invalid:
            print('\nDo you have to upload [blue]more than one file[/]? (y/n)')
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

    print('\nDo you have any [light blue]more images[/light blue] to be plate solved? '
          '([green]Y[/green]/[red]N[/red])')
    repeat = ask_for('\n: ', 'Error', str).lower()

    if repeat == 'y':
        find_fits_dir()
        upload()
        rerun()
    if repeat == 'n':
        print('\n********************'
              ' [blue]End of Plate Solving[/blue] '
              '********************')
