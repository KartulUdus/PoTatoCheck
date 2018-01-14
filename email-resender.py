#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging, csv, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from itertools import count, groupby
from threading import Thread
from utils.args import get_args

LOGIN_URL = 'https://club.pokemon.com/us/pokemon-trainer-club/login'

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(threadName)16s][%(module)14s]'
           '[%(levelname)8s] %(message)s')

log = logging.getLogger(__name__)
args = get_args()

def send(hamsters):
    for hamster in hamsters:
        potato = hamster.split(',')
        potato[-1] = potato[-1].strip()
        un = potato[1]
        pw = potato[2]
        em = re.sub('@','+{}@'.format(un), args.email)

        driver = webdriver.PhantomJS()
        driver.get(LOGIN_URL)
        try:
            WebDriverWait(driver, args.timeout).until(
                EC.title_contains('Trainer Club'))
        except TimeoutException:
            log.warn('Cannot get to trainer club')
            driver.quit()
            continue

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

            try:
                WebDriverWait(driver, args.timeout).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,
                                                    'Resend')))

                resend = driver.find_element_by_partial_link_text('Resend')
                resend.click()
                try:
                    WebDriverWait(driver, args.timeout).until(
                        EC.presence_of_element_located((By.ID, 'id_email')))
                    fem = driver.find_element_by_id('id_email')
                    feu = driver.find_element_by_id('id_username')
                    fep = driver.find_element_by_id('id_password')
                    cont = driver.find_element_by_css_selector(
                        'input.button')
                    fem.send_keys(em)
                    feu.send_keys(un)
                    fep.send_keys(pw)
                    cont.click()

                    try:
                        WebDriverWait(driver, args.timeout).until(
                            EC.text_to_be_present_in_element(
                                (By.CSS_SELECTOR,
                                 '.form-wrapper > h3:nth-child(1)'),
                                        'Thank you for creating an account!'))
                        log.info('Email re-sent for account {}'.format(un))
                        driver.quit()

                    except TimeoutException:
                        log.warn(
                            'did not get to correct page with {}'.format(un))
                        driver.save_screenshot('{}Error.png'.format(un))
                        driver.quit()
                        continue

                except TimeoutException:
                    log.warn('did not get to correct page with {}'.format(un))
                    driver.save_screenshot('{}Error.png'.format(un))
                    driver.quit()
                    continue


            except TimeoutException:
                log.warn('ignoring account {},'
                         ' e-mail already verified'.format(un))
                driver.quit()
                continue


        except TimeoutException:
            log.warn('{} is not valid'.format(un))
            driver.quit()
            continue


if __name__ == '__main__':

    log.info('email-resender is starting')

    if not args.email:
        log.critical('No e-mail set, exiting')
        exit (1)

    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
             args.email):
        log.critical('e-mail not valid format, exiting')
        exit(1)

    FILENAME = '{}'.format(args.accounts)
    try:
        ## Check how big should hamster batch be
        with open(FILENAME) as ac:
            hamsters = csv.reader(ac)
            total = (sum(1 for row in hamsters))
            jobs = total / args.threads
            if total < args.threads:
                log.critical('{} accounts, but {} threads, Need fewer '
                             'threads'.format(total,args.threads))
                exit(1)

        with open(FILENAME) as ac:
            ## Calculate optimal amout of hamsters to send to worker
            for g, group in groupby(
                    ac, key=lambda _, c=count(): c.next() / jobs):
                t = Thread(target=send, args=(list(group),))
                t.start()
    except KeyboardInterrupt:
        print 'exiting'
        exit(1)

