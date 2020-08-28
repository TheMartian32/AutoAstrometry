from selenium import webdriver
from rich import print


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

def look_up_target():
    print(
        '\nWould you like to be [bold]redirected[/bold] to the [blue]SIMBAD search portal[/blue]?')
    redirect_simbad = ask_for('(Y/N): ').lower()

    if redirect_simbad == 'y':
        # * Getting name of target to enter into SIMBAD search portal
        print(
            '\nWhat is the [bold]name[/bold] of your [blue]target[/blue]?')
        target_name = ask_for('\n: ')

        # * Opening SIMBAD URL.
        browser = webdriver.Safari()
        browser.get('http://simbad.u-strasbg.fr/simbad/sim-fbasic')
        python_button = browser.find_element_by_xpath(
            "/html/body/div[3]/div/form/table/tbody/tr[1]/td[2]/input")
        python_button.send_keys(f'{target_name}')

        python_button = browser.find_element_by_xpath(
            "/html/body/div[3]/div/form/table/tbody/tr[3]/td[2]/input[1]")
        python_button.click()

    elif redirect_simbad == 'n':
        print('Continuing...')

if __name__ == "__main__":
    look_up_target()