import threading
import clr

clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw
COjw = Ojw()


def JoyCtrl(nJoy = 1):
    nCnt = 0
    print("Joy")
    CJoy = Ojw.CJoystick(nJoy)
    while(True):
        CJoy.Update()
        for i in range(0, 10):
            if CJoy.IsDown_Event(i) == True:
                nCnt = nCnt + 1
                print("Down:" + str(i))
                if nCnt > 3:
                    break
        if nCnt > 3:
            break

nJoyIndex=1

t = threading.Thread(target=JoyCtrl, args=(nJoyIndex))
t.start()