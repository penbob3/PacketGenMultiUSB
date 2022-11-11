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
ser = serial.Serial('COM4', 115200, timeout=1)


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

lastcapturedevent = int(time.time()) * 1000

def reportMouseEvents(event):
    global lastcapturedevent
    global counter
    newtime = int(event.time * 1000)
    #if (newtime - lastcapturedevent > 5):
    if (True):
        lastcapturedevent = newtime
        #print(event)
        dxdy = [event.x - 1280, event.y - 720]
        print(dxdy)
        mouse.move(1024, 576)
        counter += 1
        if (dxdy[0] > 0):
            pack = bytes([160, abs(dxdy[0])])
            ser.write(pack)
        elif (dxdy[0] < 0):
            pack = bytes([162, abs(dxdy[0])])
            ser.write(pack)

        if (dxdy[1] > 0):
            pack = bytes([164, abs(dxdy[1])])
            ser.write(pack)
        elif (dxdy[1] < 0):
            pack = bytes([166, abs(dxdy[1])])
            ser.write(pack)


def reportKeyEvents(event):
    if (event.name == "ctrl"):
        if (event.event_type == "down"):
            ctrl = True
        else:
            ctrl = False
    elif (event.name == "alt"):
        if (event.event_type == "down"):
            alt = True
        else:
            alt = False
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

#listenmouse = mouse.hook(reportMouseEvents)
listenkey = keyboard.hook(reportKeyEvents)

def exit_handler():
    print("Total time taken: " + str(time.time() - starttime))
    print("Total event calls: " + str(counter))

atexit.register(exit_handler)

while True:
    print("Listening...")
    time.sleep(20)