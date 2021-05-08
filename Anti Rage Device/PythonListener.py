from sys import platform
from time import sleep
from PIL import Image
import os
import serial
import keyboard

# Path to image to open on hit detected
img = Image.open("dababy.jpg")

def mac_quit():
    keyboard.press('cmd')
    keyboard.press('q')
    sleep(0.5)
    keyboard.release('q')
    keyboard.release('cmd')

def windows_quit():
    keyboard.press('alt')
    keyboard.press('f4')
    sleep(0.5)
    keyboard.release('f4')
    keyboard.release('alt')

# Ports must be changed to match the port recieveing serial data from arduino
# The arduino I have is not recognized as a keyboard so I had to hack this code together
# I wouldnt recommed this code to make this
# Get an arduino that supports keybord output and code all functionality on the arduino ide
quit_command = None
port = None
if platform == 'darwin':
    quit_command = mac_quit
    port = '/dev/cu.usbserial-14440'
elif platform == 'win32':
    quit_command = windows_quit
    port = 'COM3'

ser = serial.Serial(port, 9600)
ser.flushInput()

osu = True
if osu:
    quit_command = lambda : os.system("taskkill /IM osu!.exe /F")

while True:
    try:
        # Read serial data from arduino
        ser_bytes = ser.readline()

        # Decode data into text ex: "hit 0.9" and split on space ['hit', '0.9']
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8").split(' ')

        # Unpack into variables and turn string to float ex: '0.9' -> 0.9
        cmd, hit_force = decoded_bytes[0], float(decoded_bytes[1])
        if cmd == 'hit':

            # Threshold for hit detection
            if hit_force >= .90:
                if quit_command != None:
                    # Quit
                    quit_command()

                    # Uncomment below to show the image
                    # img.show()
                # Delay code for one second
                sleep(1)
    except Exception as e:
        print(e)
        break
