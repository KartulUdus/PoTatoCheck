# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from itertools import count, groupby
from threading import Thread
from utils.args import get_args
import csv, logging
LOGIN_URL = 'https://club.pokemon.com/us/pokemon-trainer-club/login'

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(threadName)16s][%(module)14s]'
           '[%(levelname)8s] %(message)s')

log = logging.getLogger(__name__)

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
                        driver.quit()
                        continue
                else:
                    print ','.join(potato)
                    driver.quit()
            except TimeoutException:
                continue
            finally:
                driver.quit()

        except IndexError:
            continue

if __name__ == '__main__':
 ## Declaratopms
    args = get_args()
    FILENAME = '{}'.format(args.accounts)
    try:
 ## Check how big should hamster batch be
        with open(FILENAME) as ac:
            hamsters = csv.reader(ac)
            total = (sum(1 for row in hamsters))
            jobs = total / args.threads
            if total < args.threads:
                log.critical('{} accounts, but {} threads, Need fewer '
                             'threads'.format(total, args.threads))
                exit(1)

        with open(FILENAME) as ac:
            ## Calculate optimal amout of hamsters to send to worker
            for g, group in groupby(ac, key=lambda _, c=count(): c.next()/jobs):

                t = Thread(target=check, args=(list(group),))
                t.start()
    except KeyboardInterrupt:
        print 'exiting'
        exit(1)
