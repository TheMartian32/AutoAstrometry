# * Imports
from astroquery.astrometry_net import AstrometryNet
from rich import print
import shutil
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


def domain():

    print('\n********************'
          ' Beginning of plate solving '
          '********************')

    look_for = True

    while look_for:
        # * Asks for the directory of the FITS file.
        fits_dir = ask_for(
            '\nWhat is the directory of the FITS file? (Make sure file ends in .FITS, .JPEG or .PNG): ', 'Error', str)

        # * If the the file ends with the desired type
        if fits_dir.endswith('.FITS' or '.JPEG' or '.PNG'):
            look_for = False
            break
        else:
            print('\nSorry, the file format you gave is incorrect.')
            fits_dir = ask_for(
                '\nWhat is the directory of the FITS file? (Make sure file ends in .fits): ', 'Error', str)

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
                                                    solve_timeout=1200)
        except TimeoutError as e:
            submission_id = e.args[1]
            print('\nThere was a timeout error. ( Process took to long ).')
        else:
            #! got a result, so terminate
            try_again = False

    if wcs_header:
        # * Code to execute when solve succeeds
        print('\n[green]Success![/green]')
        print('\nTo get more information of your image, '
              'please go to this URL: [blue]http://nova.astrometry.net/users/20995[/blue]')
    else:
        #! Code to execute when solve fails
        print('\n[bold red]Failed[/bold red] to solve.')


if __name__ == "__main__":
    domain()

    print('Do you have any [light blue]more images[/light blue] to be plate solved? '
          '([green]Y[/green]/[red]N[/red])')
    repeat = ask_for('\n: ', 'Error', str).lower()

    if repeat == 'y':
        domain()
    if repeat == 'n':
        print('\n********************'
              ' End of plate solving '
              '********************')
