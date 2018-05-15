#!/usr/bin/python35

"""
Author: James Hertan
Date:   May 15, 2018

DESCRIPTION: nudge my cursor from time to time.

"""
import time
import pyautogui

def get_current_position():
    current_x, current_y  = pyautogui.position()
    print(current_x, current_y)

    return (current_x, current_y)


def sleepy(delay=5, y_max=1999):
    y_max = 1999

    while True:
        time.sleep(delay)
        pyautogui.moveRel(xOffset=0, yOffset=1)
        x, y = get_current_position()

        if y == y_max:
            pyautogui.moveTo(0, 0)

def main():
    pyautogui.FAILSAFE = False

    # delay = 5
    # time.sleep(delay)
    # get_current_position()
    # pyautogui.moveRel(xOffset=0, yOffset=1)
    # get_current_position()

    sleepy()

if __name__ == "__main__": main()
