# * Imports
from astroquery.astrometry_net import AstrometryNet
from rich import print
import os
import webbrowser
import time


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


def upload():
    """
    Using astroquery it asks the user for the
    FITS file then it uploads that file to nova.astronometry.net
    then it solves the image, then redirects the user to the website.
    """

    look_for = True

    while look_for:
        # * Asks for the directory of the FITS file.
        fits_dir = ask_for(
            '\nWhat is the path to the FITS file? (Make sure file ends in .FITS, .JPEG or .PNG): ', 'Error', str)

        # * If the the file ends with the desired type
        if fits_dir.endswith('.FITS' or '.JPEG' or '.PNG' or '.FIT' or '.fits' or '.fit' or '.fts'):
            look_for = False
            break
        else:
            # * Tells user that the file extension that was at the end of their file was incorrect. It then repeats this loop.
            print('\nSorry, the file extension you gave is incorrect.')

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
                                                    solve_timeout=900)
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

        # * Telling user that they are currently being redirected to website.
        print('\nRedirecting you to [bold]website[/bold].')
        time.sleep(5)

        # * Opening URL
        #! If you are using this script please sign up for an account,
        #! then click on your images, then copy that URL and paste it here.
        webbrowser.open('http://nova.astrometry.net/users/20995')
    else:
        #! Code to execute when solve fails
        print('\n[bold red]Failed[/bold red] to solve.')


def domain():
    """
    Using the upload function, it asks the user how many files they need to upload
    then it loops over the upload function for every file you have.
    """

    print('\n********************'
          ' [blue]Beginning of plate solving[/blue] '
          '********************')

    how_many = ask_for(
        '\nDo you have more than one file that needs to be plate solved? (y/n): ', 'Error', str).lower()

    if how_many == 'n':
        # * Uploads one file
        upload()

    elif how_many == 'y':
        num_files = ask_for(
            '\nHow many files do you have that need to be uploaded?: ', 'Not the right data type.', _type=int)

        for i in range(num_files):
            # * For every file the user needs to upload, it calls the upload function.
            upload()


if __name__ == "__main__":
    domain()

    print('Do you have any [light blue]more images[/light blue] to be plate solved? '
          '([green]Y[/green]/[red]N[/red])')
    repeat = ask_for('\n: ', 'Error', str).lower()

    if repeat == 'y':
        domain()
    if repeat == 'n':
        print('\n********************'
              ' [blue]End of plate solving[/blue] '
              '********************')
