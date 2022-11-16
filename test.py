
import time
import atexit
import mouse
import keyboard

def reportMouseEvents(event):
    if (isinstance(event, mouse.WheelEvent)):
        print(event)

listenmouse = mouse.hook(reportMouseEvents)

while True:
    print("Listening...")
    time.sleep(5)