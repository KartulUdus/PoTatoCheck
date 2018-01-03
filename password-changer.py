#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging, csv, os, errno
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from itertools import count, groupby
from threading import Thread
from utils.args import get_args

LOGIN_URL = 'https://club.pokemon.com/us/pokemon-trainer-club/login'

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s')

log = logging.getLogger(__name__)
args = get_args()

if args.outfile:
    outfile = args.outfile
    log.info('using outfile {}'.format(args.outfile))
else:
    outfile = 'changed-password.csv'
    log.info('using default outfile changed-password.csv')


def verify_password():

    if not args.new_password:
        log.critical('No new password set, exiting')
        exit (1)

    sym = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
    s = args.new_password
    rules = [lambda s: any(x.isupper() for x in s),
             # must have at least one uppercase
             lambda s: any(x.islower() for x in s),
             # must have at least one lowercase
             lambda s: any(x.isdigit() for x in s),
             # must have at least one digit
             lambda s: any(x in sym for x in s),
             # must have symbol
             lambda s: len(s) >= 8,
             # must be at least 8 characters
             lambda s: len(s) <= 20
             # must be less than 20 characters
             ]
    if all(rule(s) for rule in rules):
        return True
    else:
        log.critical('invalid password format, exiting')
        exit(1)

def create_or_delete_outfile(file):

    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:
            print ('no outfile')
            raise

def change(hamsters):
    for hamster in hamsters:
        potato = hamster.split(',')
        potato[-1] = potato[-1].strip()
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
        except TimeoutException:
            log.warn('{} is not valid'.format(un))
            fd = open('document.csv', 'ab')
            fd.write(','.join(potato))
            fd.write('\n')
            fd.close()
            break

        try:
            WebDriverWait(driver, args.timeout).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*["
                                                "@id=\"account\"]/fieldset[1]/div/div/a[2]")))
        except TimeoutException:
            log.warn('{} has not validated e-mail'.format(un))
            fd = open('document.csv', 'ab')
            fd.write(','.join(potato))
            fd.write('\n')
            fd.close()
            driver.quit()
            break


if __name__ == '__main__':
    log.info('password-changer is starting')


    create_or_delete_outfile(outfile)
    if verify_password():
        log.info('New password meets requirements')
        FILENAME = '{}'.format(args.accounts)
        try:
            ## Check how big should hamster batch be
            with open(FILENAME) as ac:
                hamsters = csv.reader(ac)
                jobs = (sum(1 for row in hamsters)) / args.threads

            with open(FILENAME) as ac:
                ## Calculate optimal amout of hamsters to send to worker
                for g, group in groupby(
                        ac, key=lambda _, c=count(): c.next() / jobs):
                    t = Thread(target=change, args=(list(group),))
                    t.start()
        except KeyboardInterrupt:
            print 'exiting'
            exit(1)

