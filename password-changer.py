#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging, csv, os
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
        log.info('removed old outfile {}'.format(file))
    except OSError:
        log.info('Outfile doesn\'t exist, creating {}'.format(file))
    with open(file, "w"):
        log.info('created outfile {}'.format(file))



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

        if pw == args.new_password:
            log.warn('{}s password is identical to new password, '
                     'skipping'.format(un))
            fd = open(outfile, 'ab')
            fd.write(','.join(potato))
            fd.write('\n')
            fd.close()
            log.info('writing account {} to {}'.format(un, outfile))
            continue

        try:
            WebDriverWait(driver, args.timeout).until(
                EC.title_contains('Official'))

            try:
                WebDriverWait(driver, args.timeout).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,
                                                    'Password')))

                changepw = driver.find_element_by_partial_link_text('Password')
                changepw.click()
                try:
                    WebDriverWait(driver, args.timeout).until(
                        EC.presence_of_element_located((By.ID, 'id_password')))
                    oldpw = driver.find_element_by_id('id_current_password')
                    new1 = driver.find_element_by_id('id_password')
                    new2 = driver.find_element_by_id('id_confirm_password')
                    conf = driver.find_element_by_css_selector(
                        'input.button.button-green.right.match')
                    oldpw.send_keys(pw)
                    new1.send_keys(args.new_password)
                    new2.send_keys(args.new_password)
                    conf.click()

                    try:
                        WebDriverWait(driver, args.timeout).until(
                            EC.text_to_be_present_in_element(
                                (By.CSS_SELECTOR,
                                 '.column-9 > p:nth-child(2)'),
                                                'password has been updated.'))

                        fd = open(outfile, 'ab')
                        fd.write('ptc,{},{}\n'.format(un,args.new_password))
                        fd.close()
                        log.info(
                            'password changed for account {}'.format(un))
                        driver.quit()

                    except TimeoutException:
                        log.warn(
                            'did not get to correct page with {}'.format(un))
                        if not args.ignore_bad:
                            fd = open(outfile, 'ab')
                            fd.write(','.join(potato))
                            fd.write('\n')
                            fd.close()
                            log.info(
                                'writing account {} to {}'.format(un, outfile))
                            driver.save_screenshot('{}Error.png'.format(un))
                            driver.quit()
                        else:
                            log.info('ignoring account {}'.format(un))
                            driver.save_screenshot('{}Error.png'.format(un))
                            driver.quit()
                            continue

                except TimeoutException:
                    log.warn('did not get to correct page with {}'.format(un))
                    if not args.ignore_bad:
                        fd = open(outfile, 'ab')
                        fd.write(','.join(potato))
                        fd.write('\n')
                        fd.close()
                        log.info(
                            'writing account {} to {}'.format(un, outfile))
                    else:
                        log.info('ignoring account {}'.format(un))
                    driver.save_screenshot('{}Error.png'.format(un))
                    driver.quit()
                    continue


            except TimeoutException:
                log.warn('{} has not validated e-mail'.format(un))
                if not args.ignore_bad:
                    fd = open(outfile, 'ab')
                    fd.write(','.join(potato))
                    fd.write('\n')
                    fd.close()
                    log.info('writing account {} to {}'.format(un, outfile))
                else:
                    log.info('ignoring account {}'.format(un))
                driver.quit()
                continue


        except TimeoutException:
            log.warn('{} is not valid'.format(un))
            if not args.ignore_bad:
                fd = open(outfile, 'ab')
                fd.write(','.join(potato))
                fd.write('\n')
                fd.close()
                log.info('writing account {} to {}'.format(un,outfile))
            else:
                log.info('ignoring account {}'.format(un))
            driver.quit()
            continue




if __name__ == '__main__':

    log.info('password-changer is starting')

    if args.outfile == args.accounts:
        log.critical('you can\'t have the same input and output file silly!')
        exit(1)

    create_or_delete_outfile(outfile)
    if verify_password():
        log.info('New password meets requirements')
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
                    t = Thread(target=change, args=(list(group),))
                    t.start()
        except KeyboardInterrupt:
            print 'exiting'
            exit(1)

