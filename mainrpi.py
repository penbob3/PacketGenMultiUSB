#KBD = 168
#Move X + No Multi = 160
#Move X - No Multi = 162
#Move Y + No Multi = 164
#Move Y - No Multi = 166

import time
import atexit
import threading
import mouse
import keyboard
import serial
import os
from dotenv import load_dotenv
load_dotenv()

ser = serial.Serial(os.getenv('SERIAL_PORT'), 115200, timeout=1)

#while True:
#    h = bytes([168])
#    char = ("b").encode("utf8")
#    msg = h + char
#    ser.write(h)
#    ser.write(char)
#    print("Send b")
#    print(h)
#    print(char)
#    time.sleep(5)

ctrl = False
alt = False
shift = False

screenwidth = int(os.getenv('SCREEN_WIDTH'))
screenheight = int(os.getenv('SCREEN_HEIGHT'))

lastcapturedevent = int(time.time()) * 1000

def reportMouseEvents(event):
    global lastcapturedevent
    global counter
    if (isinstance(event, mouse.MoveEvent)):
        newtime = int(event.time * 1000)
        if (newtime - lastcapturedevent > 20):
        #if (True):
            lastcapturedevent = newtime
            print(event)
            dxdy = [event.x - screenwidth, event.y - screenheight]
            print(dxdy)
            mouse.move(screenwidth, screenheight)
            counter += 1
            if (dxdy[0] > 0):
                if (abs(dxdy[0]) <= 255):
                    pack = bytes([160, abs(dxdy[0])])
                else:
                    pack = bytes([160, 255])
                ser.write(pack)
            elif (dxdy[0] < 0):
                if (abs(dxdy[0]) <= 255):
                    pack = bytes([162, abs(dxdy[0])])
                else:
                    pack = bytes([162, 255])
                ser.write(pack)

            if (dxdy[1] > 0):
                if (abs(dxdy[1]) <= 255):
                    pack = bytes([164, abs(dxdy[1])])
                else:
                    pack = bytes([164, 255])
                ser.write(pack)
            elif (dxdy[1] < 0):
                if (abs(dxdy[1]) <= 255):
                    pack = bytes([166, abs(dxdy[1])])
                else:
                    pack = bytes([166, 255])
                ser.write(pack)
    elif (isinstance(event, mouse.ButtonEvent)):
        print(event)
        if (event.event_type == "down"):
            if (event.button == "left"):
                pack = bytes([188, 0])
            elif (event.button == "right"):
                pack = bytes([188, 1])
            else:
                pack = bytes([188, 2])
            ser.write(pack)
        elif (event.event_type == "up"):
            if (event.button == "left"):
                pack = bytes([190, 0])
            elif (event.button == "right"):
                pack = bytes([190, 1])
            else:
                pack = bytes([190, 2])
            ser.write(pack)


def reportKeyEvents(event):
    if (event.name == "ctrl"):
        if (event.event_type == "down"):
            pack = bytes([201, 0])
        else:
            pack = bytes([200, 0])
        ser.write(pack)
    elif (event.name == "alt"):
        if (event.event_type == "down"):
            pack = bytes([201, 1])
        else:
            pack = bytes([200, 1])
        ser.write(pack)
    elif (event.name == "shift"):
        if (event.event_type == "down"):
            pack = bytes([201, 2])
        else:
            pack = bytes([200, 2])
        ser.write(pack)
    #COMBINE THESE INTO A DICTIONARY THIS IS UGLY TO LOOK AT AND MAINTAIN
    elif (event.name == "space" and event.event_type == "up"):
        h = bytes([168])
        char = (" ").encode("utf8")
        ser.write(h)
        ser.write(char)
    elif (event.name == "enter" and event.event_type == "up"):
        h = bytes([182])
        char = (" ").encode("utf8")
        ser.write(h)
        ser.write(char)
    elif (event.name == "backspace" and event.event_type == "up"):
        h = bytes([184])
        char = (" ").encode("utf8")
        ser.write(h)
        ser.write(char)
    elif (event.name == "tab" and event.event_type == "up"):
        h = bytes([186])
        char = (" ").encode("utf8")
        ser.write(h)
        ser.write(char)
    elif (event.name == "insert" and event.event_type == "up"):
        pack = bytes([176, 0])
        ser.write(pack)
    elif (len(event.name) == 1 and event.event_type == "up"):
        print(event.event_type)
        print(event.name)
        h = bytes([168])
        char = (event.name).encode("utf8")
        ser.write(h)
        ser.write(char)
    else:
        print("Overlength code:" + event.name)


counter = 0
starttime = time.time()

listenmouse = mouse.hook(reportMouseEvents)
listenkey = keyboard.hook(reportKeyEvents)

def exit_handler():
    print("Total time taken: " + str(time.time() - starttime))
    print("Total event calls: " + str(counter))

atexit.register(exit_handler)

pack = bytes([120, 255])
ser.write(pack)

while True:
    print("Listening...")
    time.sleep(20)
