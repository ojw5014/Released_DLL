import threading
# pip install pythonnet 으로 설치
import clr
clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw

m_nDir_X = -1 
m_nDir_Y = 1
m_nDir_H = 1

m_fRange_XY = 40
m_fRange_H_Max = -150
m_fRange_H_Min = -80
m_bMinus = False
if (m_fRange_H_Max < 0) :
    m_bMinus = True
    
m_nProgEnd = 0
COjw = Ojw()
m_CMot = Ojw.CProtocol2()
m_fX = 0
m_fY = 0
m_fH = 200
m_fPan = 0
m_fTilt = 0
m_fPan_Max = 45
m_fPan_Min = -45
m_fTilt_Max = 45
m_fTilt_Min = -45
m_fInitPos_Height = 100

m_bInit = False
def Move(x,y,h, nTime, nDelay = 0):
    global m_fX
    global m_fY
    global m_fH
    
    m_fX = x
    m_fY = y
    m_fH = h
    m_CMot.Move_Delta(0, m_fX, m_fY, m_fH, nTime, nDelay)

def JoyControl(nJoy=-1):
    global m_nProgEnd
    global m_CMot
    global m_fX
    global m_fY
    global m_fH
    global m_bInit
    global m_fPan
    global m_fPan_Max
    global m_fPan_Min
    global m_fTilt
    global m_fTilt_Max
    global m_fTilt_Min
    global m_fInitPos_Height

    
    
    # nJoy = 1
    CTmr = Ojw.CTimer()
    CTmr.Set()
    if (nJoy < 0) :
        for i in range(0, 4):
            CJoy = Ojw.CJoystick(i)
            CJoy.Update()
            if (CJoy.IsValid) : 
                nJoy = i
                print("Find -> " + Ojw.CConvert.IntToStr(i))
                break

    CJoy = Ojw.CJoystick(nJoy)
    afJoy = [0,0,0,0,0,0]
    nSpeed = 2
    nSpeed_Max = 20
    nSpeed_Min = 1
    while(m_nProgEnd == 0):
        if (m_bInit == False) :
            continue
        CJoy.Update()
        for i in range(0, 10):
            if CJoy.IsDown_Event(i) == True:
                print("Down:" + str(i))
                if i == 7: # Button (Back)
                    m_nProgEnd = 1
                if i == 6: # Speed Up
                    nSpeed = nSpeed + 1
                    if (nSpeed > nSpeed_Max) :
                        nSpeed = nSpeed_Max
                    print("Speed Up: " + str(nSpeed))
                if i == 5: # Speed Down
                    nSpeed = nSpeed - 1
                    if (nSpeed < nSpeed_Min) :
                        nSpeed = nSpeed_Min
                    print("Speed Down: " + str(nSpeed))
                if i == 1: # Init Pos(Head)
                    print("Init Pos(Head)")
                    m_fPan = 0
                    m_fTilt = 0
                    m_CMot.Set(4, m_fPan)
                    m_CMot.Set(5, m_fTilt)
                    nTime_Head = 1
                    nDelay_Head = 0
                    m_CMot.Move_NoWait(nTime_Head, nDelay_Head, False) # Time, Delay
                if i == 2: # Init Pos(Body)
                    print("Init Pos(Body)")
                    Move(0, 0, m_fInitPos_Height, 1000)
        for i in range(0, 6):
            afJoy[i] = round((CJoy.GetPos(i) - 0.5) * 2, 1)
        # if (CTmr.Get() > 1000): # 1초에 한번 확인
        #     CTmr.Set()
        #     print(afJoy[0], afJoy[1], afJoy[2], afJoy[3], afJoy[4], afJoy[5])

        if (CTmr.Get() >= 50): # 100 ms에 한번 확인
            CTmr.Set()
            fRange = nSpeed # 2.0
            
            # X
            if (abs(afJoy[0]) >= 0.5):
                m_fX += afJoy[0] * fRange * m_nDir_X
                if (m_fX > m_fRange_XY) : 
                    m_fX = m_fRange_XY
                elif (m_fX < -m_fRange_XY) :
                    m_fX = -m_fRange_XY
            
            # Y
            if (abs(afJoy[1]) >= 0.5):
                m_fY -= afJoy[1] * fRange * m_nDir_Y
                if (m_fY > m_fRange_XY) : 
                    m_fY = m_fRange_XY
                elif (m_fY < -m_fRange_XY) :
                    m_fY = -m_fRange_XY
            
            # 높이
            if (abs(afJoy[3]) >= 0.5):
                m_fH += afJoy[3] * fRange * m_nDir_H
                if (m_bMinus):
                    if (m_fH < m_fRange_H_Max) : 
                        m_fH = m_fRange_H_Max
                    elif (m_fH > m_fRange_H_Min) :
                        m_fH = m_fRange_H_Min
                else:
                    if (m_fH > m_fRange_H_Max) : 
                        m_fH = m_fRange_H_Max
                    elif (m_fH < m_fRange_H_Min) :
                        m_fH = m_fRange_H_Min

            #print(m_fX, m_fY, m_fH)
            m_CMot.Move_Delta(0, m_fX, m_fY, m_fH, 1, 0, True)
            bPovEvent = False
            if CJoy.IsDown(Ojw.CJoystick.PadKey.POVLeft) == True:
                m_fPan -= fRange
                bPovEvent = True
            elif CJoy.IsDown(Ojw.CJoystick.PadKey.POVRight) == True:
                m_fPan += fRange
                bPovEvent = True
            elif CJoy.IsDown(Ojw.CJoystick.PadKey.POVUp) == True:
                m_fTilt -= fRange
                bPovEvent = True
            elif CJoy.IsDown(Ojw.CJoystick.PadKey.POVDown) == True:
                m_fTilt += fRange
                bPovEvent = True
            
            if bPovEvent == True:
                if m_fPan < m_fPan_Min:
                    m_fPan = m_fPan_Min
                if m_fPan > m_fPan_Max:
                    m_fPan = m_fPan_Max
                if m_fTilt > m_fTilt_Max:
                    m_fTilt = m_fTilt_Max
                if m_fTilt < m_fTilt_Min:
                    m_fTilt = m_fTilt_Min
                print("Pan=" + str(round(m_fPan,0)) + ", Tilt=" + str(round(m_fTilt,0)))
                m_CMot.Set(4, m_fPan)
                m_CMot.Set(5, m_fTilt)
                nTime_Head = 1
                nDelay_Head = 0
                m_CMot.Move_NoWait(nTime_Head, nDelay_Head, False) # Time, Delay

        if m_nProgEnd != 0:
            break

nJoyIndex = -1 # -1 ==> Auto Find
t = threading.Thread(target = JoyControl, args = (nJoyIndex,))
t.start()

# 통신포트 열어주기
m_CMot.Open(8, 1000000)


# 1, 2번 다이나믹셀의 위치 읽어오기
# m_CMot.SyncRead(1)
# m_CMot.SyncRead(2)
# m_CMot.SyncRead(3)
# m_CMot.SyncRead(4)
m_CMot.SyncRead(1,2,3,4,5)
print(m_CMot.GetAngle(1), m_CMot.GetAngle(2), m_CMot.GetAngle(3))

# 토크를 넣어준다.
m_CMot.SetTorq(True)



m_CMot.Delta_Clear()
m_CMot.Delta_Add(0, 1, 2, 3, 62, 70, 106, 20)

m_CMot.Move_Delta(0, m_fX, m_fY, m_fH, 1000)

fTestRange = 30 #50
fTestHeight = m_fInitPos_Height
fTestHeight_Gap = 25
if m_bMinus :
    fTestHeight = fTestHeight * -1
    m_fInitPos_Height = fTestHeight # 기준값을 축에 맞에 재 변경
    fTestHeight_Gap = fTestHeight_Gap * -1
# for i in range(0,10):
#     print(i)
#     m_CMot.Wait(1000)



try:
    # Move(fTestRange, fTestRange, fTestHeight, 1000)
    # Move(-fTestRange, fTestRange, fTestHeight, 1000)
    # Move(-fTestRange, -fTestRange, fTestHeight, 1000)
    # Move(fTestRange, -fTestRange, fTestHeight, 1000)

    # Move(fTestRange, -fTestRange, fTestHeight + fTestHeight_Gap, 1000)
    # Move(fTestRange, fTestRange, fTestHeight + fTestHeight_Gap, 1000)
    # Move(-fTestRange, fTestRange, fTestHeight + fTestHeight_Gap, 1000)
    # Move(-fTestRange, -fTestRange, fTestHeight + fTestHeight_Gap, 1000)

    # Move(-fTestRange, -fTestRange, fTestHeight + fTestHeight_Gap*2, 1000)
    # Move(fTestRange, -fTestRange, fTestHeight + fTestHeight_Gap*2, 1000)
    # Move(fTestRange, fTestRange, fTestHeight + fTestHeight_Gap*2, 1000)
    # Move(-fTestRange, fTestRange, fTestHeight + fTestHeight_Gap*2, 1000)

    Move(0, 0, fTestHeight, 1000)

    m_CMot.Set(4, m_fPan)
    m_CMot.Set(5, m_fTilt)
    nTime_Head = 1
    nDelay_Head = 0
    m_CMot.Move_NoWait(nTime_Head, nDelay_Head, False) # Time, Delay
    
    m_bInit = True

    while(m_nProgEnd == 0):
        m_CMot.Wait(1000)
    
except KeyboardInterrupt:
    print("Received interrupt. Exiting program.")
    m_nProgEnd = 1

# 통신을 닫는다.
m_CMot.Close()