#!/usr/bin/python
# -*- coding: utf-8 -*-
import configargparse
import os
import sys
import psutil


def get_args():

    configfile = []
    if '-cf' not in sys.argv and '--config' not in sys.argv:
        configfile = [os.getenv('CONFIG', os.path.join(
            os.path.dirname(__file__), '../config/config.ini'))]
    parser = configargparse.ArgParser(
        default_config_files=configfile, description='Potato-Check-tools')
    lcores = psutil.cpu_count(logical=True)
    parser.add_argument(
        '-ac',
        '--accounts',
        help='path to account file. ex: accounts.csv',
        required=True)

    parser.add_argument(
        '-of',
        '--outfile',
        help='path to output file. ex: verified.csv',
        default=False
        )

    parser.add_argument(
        '-ib',
        '--ignore-bad',
        help='don\'t store unverified accounts',
        action='store_true',
        default=False
        )

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

    parser.add_argument('-npw', '--new-password',
                        help=('New password to change to'),
                        type=str, default=False)

    return parser.parse_args()