"""
SWGOH.GG Mod Tool
"""

import time
import os
from selenium import webdriver

from swgoh.gg.columns import Columns
from swgoh.gg.mod import Mod
from com.progress import progress_bar
import csv
import argparse

from swgoh.timer import Timer


def get_mods_selenium(user, web_address, pct_opt, web_browser="chrome", resource=""):

    duration = 2  # Sleep time between http get requests

    if web_browser.lower() == "chrome":
        browser = webdriver.Chrome()
    elif web_browser.lower() == "firefox":
        browser = webdriver.Firefox()
    else:
        return

    try:
        http = "http://"
        page = "/?page={}"
        browser.get(http+web_address+resource+page.format(1))

        activity = "Building Mods"
        page_activity = "Building Mods for page [{}]"
        total_mods = 0

        # Get first page navigation and page total
        page_elm = browser.find_element_by_class_name("pagination")
        current_page, total_pages = get_pages(page_elm)

        mod_list = []

        # Loop over all the pages
        for j in range(total_pages):
            j += 1  # Start on Page 1
            print("Reading mods on page [%i of %i]" % (j, total_pages))

            # Get all mod elements on this page
            mods = browser.find_elements_by_class_name("collection-mod")
            page_mods = len(mods)
            total_mods += page_mods  # Add to total mods

            if len(mods) > 0:
                print("Total mods on page %i: [%i]" % (j, page_mods))
            elif total_mods == 0:
                raise ValueError("No mods found on page: %i" % j)

            build_time = 0
            clock = Timer()
            progress_bar(page_activity.format(j), page_mods, 0, build_time)

            for index, mod in enumerate(mods):
                clock.start()

                new_mod = Mod(mod)
                new_mod.build_mod()
                mod_list.append(new_mod)

                clock.end()
                build_time += clock.elapsed
                clock.reset()
                progress_bar(page_activity.format(j), page_mods, index+1, build_time)

            new_line()

            # Navigate to next page
            if j < total_pages:
                browser.get(http+web_address+resource+page.format(j+1))
                time.sleep(duration)

        new_line()

        print("Total mods for user %s: %i" % (user, total_mods))

        # Write sec aggregate to csv
        write_sec_agg_csv(mod_list)

    except Exception as e:  # Catch all exceptions and close the browser.
        browser.quit()
        raise e

    browser.quit()
    return 0


def new_line():
    print("")


def get_pages(page_elm):
    current = 0
    total = 0

    values = page_elm.text.split(" ")
    if len(values) == 4:
        current = values[1].strip()
        total = values[3].split("\n")[0]

    return current, int(total)


def write_csv(mod_list):
    filename = "swgoh_mods" + "-" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    abs_path = os.path.join(os.curdir, "output")

    headers = ["Slot", "Set", "Pips", "Level", "Character", "primary_stat", "primary_value",
               "1_secondary_stat", "1_secondary_value",
               "2_secondary_stat", "2_secondary_value",
               "3_secondary_stat", "3_secondary_value",
               "4_secondary_stat", "4_secondary_value"]

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


def write_sec_agg_csv(mod_list):
    filename = "swgoh_mods" + "-" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    abs_path = os.path.join(os.curdir, "output")

    headers = []
    for col in Columns.ICOL.values():
        headers.append(col.name)

    os.chdir(abs_path)
    errors = []
    with open(filename, 'w', newline='') as myfile:
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
            mod.to_csv_sec_agg(line, pct)
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
            print("Details:")
            for index, error in enumerate(errors):
                print("%i: %s" % (index, error))
        else:
            print("CSV Location: %s" % os.path.join(os.getcwd(), "output", filename))


def print_html(browser):
    html = browser.page_source
    print("html: %s" % html)

if __name__ == '__main__':

    print("GG Mods tool v1")
    parser = argparse.ArgumentParser(description="GG Mods Tool")
    parser.add_argument("-b", "--browser", required=False, help="Web Browser (Chrome or Firefox). Defaults to Chrome")
    parser.add_argument("-u", "--user", required=True, help="SWGOH userid")
    parser.add_argument("-p", "--pct", action="store_true", default=False, required=False,
                        help="Show percent symbol in csv output.")
    args = vars(parser.parse_args())

    wb = args.get('browser')
    swgoh_user = args.get('user')
    pct = args.get('pct')

    # SWGOH.GG
    address = "swgoh.gg/u/" + swgoh_user
    res_mods = "/mods"

    print("Requesting Mods from: %s" % address + res_mods)

    rc = get_mods_selenium(swgoh_user, address, pct, wb, res_mods)

    print("Mods tool return code: %i" % rc)

    #write_sec_agg_csv(None)


