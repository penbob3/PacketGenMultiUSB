ba = bytes("@", "utf-8")
print(ba)
b = [64]
b = bytes(b)
s = b.decode("UTF-8")
print(s)

# 2 Byte encoding method
# First byte determines action
# 1 is 

#KBD = 168
#Move X + No Multi = 160
#Move X - No Multi = 162
#Move Y + No Multi = 164
#Move Y - No Multi = 166

a = bytes([(168).to_bytes(1, "little")[0], "a".encode("utf8")[0]])
print(list(a))

if (a[0] == 168):
    char = a[1:2].decode('utf8')
    print(char)

dxdy = []

import mouse
import time
import threading
from queue import Queue

mouseq = Queue()
kbdq = Queue()

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

#def reportKBDClicks()

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