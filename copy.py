#!/usr/bin/python35

"""
Author: James Hertan
Date:   Dec 2017

DESCRIPTION: Copy script
"""

PASSWORDS = {
    'email':    '123',
    'blog':     '456'
}

from sys import argv, exit
import pyperclip

def main():
    if len(argv) < 2:
        print('Usage: python copy.py [account] - copy account pw')
        exit()

    account = argv[1]

    if account in PASSWORDS:
        pyperclip.copy(PASSWORDS[account])
        print('Password for ' + account + ' copied to clipboard.')
    else:
        print('There is no account named ' + account + '.')


if __name__ == "__main__": main()
