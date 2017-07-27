"""
Main CrouchingRancor API
"""

import time
import os
from selenium import webdriver
from swgoh.mod import Mod
from com.progress import progress_bar
import csv
import argparse

from swgoh.timer import Timer


def get_mods_selenium(user, web_address, web_browser="chrome", resource=""):

    retries = 5
    duration = 1

    if web_browser.lower() == "chrome":
        browser = webdriver.Chrome()
    elif web_browser.lower() == "firefox":
        browser = webdriver.Firefox()
    else:
        return

    http = "http://"
    browser.get(http+web_address+resource)
    name_element = browser.find_element_by_class_name("form-control")
    name_element.clear()
    name_element.send_keys(swgoh_user)

    enter_button = browser.find_element_by_class_name("btn-default")
    enter_button.click()

    activity = "Building Mods"
    total_mods = 0

    for i in range(retries):
        time.sleep(duration)

        mods = browser.find_elements_by_class_name("modAsset")
        total_mods = len(mods)

        if total_mods > 0:
            print("Total mods for %s: %i" % (user, total_mods))
            new_line()
            break
        elif i < retries:
            print("Sleeping for %i, then retrying." % duration)

    if total_mods == 0:
        print("No mods found, retries(%i) exhausted." % retries)
        return -1

    build_time = 0
    clock = Timer()
    progress_bar(activity, total_mods, 0, build_time)

    mod_list = []
    for index, mod in enumerate(mods):
        clock.start()

        new_mod = Mod(mod)
        new_mod.build_mod()
        mod_list.append(new_mod)

        clock.end()
        build_time += clock.elapsed
        clock.reset()
        progress_bar(activity, total_mods, index+1, build_time)

    new_line()

    # Write to csv
    write_csv(mod_list)

    browser.quit()
    return 0


def new_line():
    print("")


def write_csv(mod_list):
    filename = "swgoh_mods" + "-" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    abs_path = os.path.join(os.curdir, "output")

    headers = ["Slot", "Set", "Pips", "Level", "Rating", "Character", "primary_stat", "primary_value",
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

        activity = "Writing csv"
        total_mods = len(mod_list)
        clock = Timer()
        build_time = 0
        progress_bar(activity, total_mods, 0, build_time)
        for index, mod in enumerate(mod_list):
            clock.start()
            line = []
            mod.to_csv(line)
            try:
                wr.writerow(line)
            except UnicodeEncodeError:
                index_str = str(index)
                error_line = "Error processing mod: " + index_str
                errors.append(error_line)
            clock.end()
            build_time += clock.elapsed
            clock.reset()
            progress_bar(activity, total_mods, index+1, build_time)

        new_line()
        if len(errors) > 0:
            print("Done, with %i errors." % len(errors))
            print("Detais:")
            for index, error in enumerate(errors):
                print("%i: %s" % (index, error))


def print_html(browser):
    html = browser.page_source
    print("html: %s" % html)

if __name__ == '__main__':

    print("Mods tool v1")
    parser = argparse.ArgumentParser(description="Mods Tool")
    parser.add_argument("-b", "--browser", required=False, help="Web Browser (Chrome or Firefox). Defaults to Chrome")
    parser.add_argument("-u", "--user", required=True, help="SWGOH userid")
    args = vars(parser.parse_args())

    wb = args.get('browser')
    swgoh_user = args.get('user')

    # CrouchingRancor Resources
    address = "apps.crouchingrancor.com"
    res_mods = "/Mods/Manager"
    res_settings = "/Settings"

    print("Requesting Mods from: %s" % address)

    rc = get_mods_selenium(swgoh_user, address, wb, res_mods)

    print("Mods tool return code: %i" % rc)
