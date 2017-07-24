"""
Main CrouchingRancor API
"""

import time
from selenium import webdriver
from swgoh.mod import Mod
from com.file_writer import *
import csv


def get_mods_selenium(user, web_address, resource=""):
    browser = webdriver.Firefox()
    http = "http://"
    browser.get(http+web_address+resource)
    name_element = browser.find_element_by_class_name("form-control")
    name_element.clear()
    name_element.send_keys(swgoh_user)

    enter_button = browser.find_element_by_class_name("btn-default")
    enter_button.click()
    time.sleep(5)

    mods = browser.find_elements_by_class_name("modAsset")
    print("Total mods for %s: %i" % (user, len(mods)))
    new_line()

    mod_list = []
    for index, mod in enumerate(mods):
        pct = (index+1) / len(mods)
        complete = int((pct*100))
        p = int((complete/4))
        state = "#" * p
        blanks = " " * (24 - p)
        print("\rReading Mods...[%s %s%i%%]" % (state, blanks, complete), end='')

        new_mod = Mod(mod)
        new_mod.build_mod()
        mod_list.append(new_mod)

    new_line()
    print("Done.")

        # print("*** Mod %i ***" % (index+1))
        # new_mod.print_self()
        # print("*** End of Mod: %i ***" % (index+1))
        #new_line()

    # Write to csv
    write_csv(mod_list)

    browser.quit()
    return 0


def new_line():
    print("")


def write_csv(mod_list):
    filename = "swgoh_mods" + "-" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    abs_path = os.path.join(os.curdir, "output")

    headers = ["Pips", "Level", "Rating", "Character", "primary_stat", "primary_value",
               "1_secondary_stat", "1_secondary_value", "1_secondary_rating",
               "2_secondary_stat", "2_secondary_value", "2_secondary_rating",
               "3_secondary_stat", "3_secondary_value", "3_secondary_rating",
               "4_secondary_stat", "4_secondary_value", "4_secondary_rating"]

    os.chdir(abs_path)
    errors = []
    with open(filename, 'w', newline='') as myfile:
        #  wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr = csv.writer(myfile)
        wr.writerow(headers)

        state = ""
        for index, mod in enumerate(mod_list):
            pct = (index+1) / len(mod_list)
            complete = int((pct*100))
            p = int(complete/4)
            state = "#" * p
            blanks = " " * (24 - p)
            print("\rWriting csv....[%s %s%i%%]" % (state, blanks, complete), end='')

            line = []
            mod.toCsv(line)
            try:
                wr.writerow(line)
            except UnicodeEncodeError:
                index_str = str(index)
                error_line = "Error processing mod: " + index_str
                errors.append(error_line)

        new_line()
        if len(errors) == 0:
            print("Done.")
        else:
            print("Done, with %i errors." % len(errors))
            print("Detais:")
            for index, error in enumerate(errors):
                print("%i: %s" % (index, error))


def print_html(browser):
    html = browser.page_source
    print("html: %s" % html)

if __name__ == '__main__':

    print("Crouching tool v1")

    # CrouchingRancor Resources
    address = "apps.crouchingrancor.com"
    res_mods = "/Mods/Manager"
    res_settings = "/Settings"

    # SWGOH user
    swgoh_user = "boozie"

    print("Requesting Mods from: %s" % address)

    rc = get_mods_selenium(swgoh_user, address, res_mods)

    print ("CrouchingRancor tool return code: %i" % rc)
