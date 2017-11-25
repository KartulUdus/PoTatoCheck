# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from itertools import count, groupby
import psutil
import multiprocessing
import csv
import configargparse
LOGIN_URL = 'https://club.pokemon.com/us/pokemon-trainer-club/login'

def get_args():
    parser = configargparse.ArgParser(description='PTC-Login-Check')
    lcores = psutil.cpu_count(logical=True)
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
        default=5),

    parser.add_argument(
        '-th',
        '--threads',
        help='how many processes to run in',
        type=int,
        default=lcores)

    parser.add_argument(
        '-iu',
        '--ignoreunactivated',
        help='Ignore accounts with unactivated e-mail',
        action='store_true',
        default=False)
    return parser.parse_args()

def check(hamsters):

    args = get_args()
    for hamster in hamsters:
        potato = hamster.split(',')
        potato[-1] = potato[-1].strip()
        try:
            un = potato[1]
            pw = potato[2]
            driver = webdriver.PhantomJS()
            driver.get(LOGIN_URL)
            WebDriverWait(driver, args.timeout).until(
            EC.title_contains('Trainer Club'))
            user = driver.find_element_by_id('username')
            passw = driver.find_element_by_id('password')
            user.clear()
            user.send_keys(un)
            passw.clear()
            passw.send_keys(pw)
            passw.send_keys(Keys.RETURN)
            try:
                WebDriverWait(driver, args.timeout).until(
                    EC.title_contains('Official'))
                if args.ignoreunactivated:
                    try:
                         if driver.find_element_by_id('id_country')>0:
                            print ','.join(potato)
                    except Exception:
                        continue
                else:
                    print ','.join(potato)
            except TimeoutException:
                continue
            finally:
                driver.close()

        except IndexError:
            continue

if __name__ == '__main__':
    args = get_args()
    FILENAME = '{}'.format(args.accounts)
    with open(FILENAME) as ac:
        hamsters = csv.reader(ac)
        jobs = (sum (1 for row in hamsters))/args.threads
    with open(FILENAME) as ac:
        for g, group in groupby(ac, key=lambda _, c=count(): c.next()/jobs):
            job = []
            for i in range(args.threads):
                 potato = list(group)
                 p = multiprocessing.Process(target=check, args=[potato])
                 job.append(p)
                 p.start()



