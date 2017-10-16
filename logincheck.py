# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import configargparse
parser = configargparse.ArgParser(description='PTC-Login-Check')
parser.add_argument(
    '-ac',
    '--accounts',
    help='path to account file. ex: accounts.csv',
    required=True)
parser.add_argument(
    '-t',
    '--timeout',
    help='timeout to wait for signed in hamster',
    type=int,
    default=5)
parser.add_argument(
    '-iu',
    '--ignoreunactivated',
    help='Ignore accounts with unactivated e-mail',
    action='store_true',
    default=False)
args = parser.parse_args()
FILENAME = "{}".format(args.accounts)


with open(FILENAME) as ac:
    hamsters = csv.reader(ac)
    for hamster in hamsters:
        un = list(hamster)[1]
        pw = list(hamster)[2]
        driver = webdriver.PhantomJS()
        driver.get("https://club.pokemon.com/us/pokemon-trainer-club/login")
        assert "Trainer Club" in driver.title
        user = driver.find_element_by_id("username")
        passw = driver.find_element_by_id("password")
        user.clear()
        user.send_keys(un)
        passw.clear()
        passw.send_keys(pw)
        passw.send_keys(Keys.RETURN)
        try:
            element = WebDriverWait(driver, args.timeout).until(
                EC.title_contains('Official'))
            if args.ignoreunactivated:
                try:
                     if driver.find_element_by_id("id_country")>0:
                        print ",".join(hamster)
                except Exception:
                    continue
            else:
                print ",".join(hamster)
        except TimeoutException:
            continue
        finally:
            driver.close()
