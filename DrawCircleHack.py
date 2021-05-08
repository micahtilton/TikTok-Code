import pyautogui
from pynput.mouse import Controller, Button
from time import sleep
from math import sin, cos, pi
from numpy import arange

sleep(5)
curr_x, curr_y = pyautogui.position()
mouse = Controller()

RADIUS = 500
STEPS = 100
TIME = 1
TIME_DELTA = TIME/STEPS
STEP_AMOUNT = 2*pi/STEPS

first = True
for angle in arange(0, 2*pi+(STEP_AMOUNT*5), STEP_AMOUNT):
    x, y = RADIUS * cos(angle), RADIUS * sin(angle)
    new_x, new_y = curr_x + x, curr_y + y
    pyautogui.moveTo(new_x, new_y, _pause=False)

    if first:
        sleep(4)
        mouse.press(Button.left)
        first = False

mouse.release(Button.left)