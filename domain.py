
# * Imports
import webbrowser
import time
from astroquery.astrometry_net import AstrometryNet
from rich import print
from astroquery.simbad import Simbad


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


def redirect(url=str):
    """
    Takes in a URL as a string and asks the user if they would like to be redirected
    to that URL.

    Args:
        url (str, optional): URL that the user needs to be redirected to. Defaults to str.
    """
    invalid = True
    while invalid:
        print(f'\nWould you like to be [blue]redirected[/blue] to: {url} ?')
        redirect = ask_for(
            '(y/n): ', error_msg='Wrong data type', _type=str).lower()

        if redirect[0] == 'y':
            webbrowser.open_new_tab(f'{url}')
            invalid = False
        elif redirect[0] == 'n':
            print('\nContinuing...')
            invalid = False


print('adding new stuff')


def simbad_query():
    """
    Looks up target and prints out the information such as RA and Dec.
    When using the function, it automatically asks the user for a target.
    """

    try:
        print(
            '\nTo find the [blue]RA and Dec[/blue] of your target, please put it in here.')
        print("If your target can't be found, it will automatically redirect you to the website to put it in again.")
        target = ask_for('\nTarget name: ')
        query = Simbad.query_object(f'{target}')
        query.pprint()
        redirect('http://simbad.u-strasbg.fr/simbad/sim-fbasic')
    except:
        webbrowser.open('http://simbad.u-strasbg.fr/simbad/sim-fbasic')


def search(image):
    search_through = image

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

    H, W = search_through.shape

    x = int((target_ra-center_ra) / pixel_scale + W / 2)
    y = int((target_dec-center_dec) / pixel_scale + H / 2)

    patch_size = 50
    image_patch = search_through[x - patch_size:x +
                                 patch_size, y - patch_size: y+patch_size]
    return image_patch


def upload():
    """
    Using astroquery it asks the user for the
    FITS file then it uploads that file to nova.astronometry.net
    then it solves the image, then redirects the user to the website.
    """

    look_for = True

    while look_for:
        # * Asks for the directory of the FITS file.
        print('\n-------------------------------------------------------')
        print('What is the path to the FITS file?')
        print(
            'Please make sure the file [bold blue]ends in .FITS, JPEG, or .PNG[/bold blue]')
        print('-------------------------------------------------------')

        fits_dir = ask_for('\n: ', str)

        # * If the the file ends with the desired type
        file_types = ['.FITS', '.JPEG', '.PNG',
                      '.FIT', '.fits', '.fit', '.fts']
        if fits_dir.endswith(tuple(file_types)):
            look_for = False

        else:
            # * Tells user that the file extension that was at the end of their file was incorrect. It then repeats this loop.
            print(
                'Sorry, the [bold white]file[/bold white] you gave is [red]incorrect[/red].')

    # * Creating instance of astrometry.net
    ast = AstrometryNet()
    ast.api_key = 'bchkvzadjuswddhg'

    try_again = True
    submission_id = None

    while try_again:
        try:
            if not submission_id:
                wcs_header = ast.solve_from_image(f'{fits_dir}',
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
        print('\n[green]Success![/green]')
        print('\nTo get the most possible information out of your image please go to the website below.')
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


def domain():
    """
    Using the upload function, it asks the user how many files they need to upload
    then it loops over the upload function for every file you have.
    """

    print('\n********************'
          ' [blue]Beginning of Plate Solving[/blue] '
          '********************')

    # * While the prompt isnt y or n it repeats it
    invalid = True
    while invalid:
        print(
            '\nDo you have [blue]more than one file[/blue] that needs to be uploaded? (y/n)')
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


if __name__ == "__main__":
    print('\n----------------------------------------------------------------------------------')
    print('To use this software please register for an account '
          'on http://nova.astrometry.net')
    print('----------------------------------------------------------------------------------')

    time.sleep(1)

    domain()

    print('\nDo you have any [light blue]more images[/light blue] to be plate solved? '
          '([green]Y[/green]/[red]N[/red])')
    repeat = ask_for('\n: ', 'Error', str).lower()

    if repeat == 'y':
        domain()
    if repeat == 'n':
        print('\n********************'
              ' [blue]End of Plate Solving[/blue] '
              '********************')
