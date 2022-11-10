#KBD = 168
#Move X + No Multi = 160
#Move X - No Multi = 162
#Move Y + No Multi = 164
#Move Y - No Multi = 166

lastxy = []
lasttime = 0

import mouse
import time
import threading
from queue import Queue

#mouseq = Queue()
#kbdq = Queue()

def reportMouseMoves(mouseq: Queue):
    while True:
        xy = mouse.get_position()
        mouse.move(1024, 576)
        #print(xy)
        dxdy = [xy[0] - 1024, xy[1] - 576]
        if ((dxdy[0] == 0 and dxdy[1] == 0) == False):
            mouseq.put(dxdy)
        #print(dxdy)
        time.sleep(0.005)

def reportMouseClicks(mouseq: Queue):
    while True:
        mouseq.put()

lastcapturedevent = int(time.time()) * 1000

def reportMouseEvents(event):
    global lastcapturedevent
    global counter
    newtime = int(event.time * 1000)
    if (newtime - lastcapturedevent > 5):
        lastcapturedevent = newtime
        #print(event)
        dxdy = [event.x - 1280, event.y - 720]
        print(dxdy)
        mouse.move(1024, 576)
        counter += 1
        #lastxy = [event.x, event.y]
    
        
counter = 0
starttime = time.time()

listen = mouse.hook(reportMouseEvents)

#def reportKBDClicks()

"""
mouseCapture = threading.Thread(target=reportMouseMoves, args=[mouseq], daemon=True)
mouseCapture.start()

clickCapture = threading.Thread(target=reportMouseClicks, args=[mouseq], daemon=True)
clickCapture.start()

while True:
    size = mouseq.qsize()
    if (size >= 1):
        if (size > 3):
            with mouseq.mutex:
                mouseq.queue.clear()
                print("Mouse move queue is overloaded! Try turning down the polling frequency!")
        #print(mouseq.qsize())
        mousemdata = mouseq.get()
        print(mousemdata)
"""

import atexit

def exit_handler():
    print("Total time taken: " + str(time.time() - starttime))
    print("Total event calls: " + str(counter))

atexit.register(exit_handler)

while True:
    print("What")
    time.sleep(0.1)