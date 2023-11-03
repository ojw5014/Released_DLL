import threading
# pip install pythonnet 으로 설치
import clr
clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw

m_nProgEnd = 0
COjw = Ojw()
m_CMot = Ojw.CProtocol2()
m_fX = 0
m_fY = 0
m_fH = 200

m_bInit = False
def Move(x,y,h, nTime, nDelay = 0):
    global m_fX
    global m_fY
    global m_fH
    
    m_fX = x
    m_fY = y
    m_fH = h
    m_CMot.Move_Delta(0, m_fX, m_fY, m_fH, nTime, nDelay)

def JoyControl(nJoy):
    global m_nProgEnd
    global m_CMot
    global m_fX
    global m_fY
    global m_fH
    global m_bInit


    
    
    # nJoy = 1
    CTmr = Ojw.CTimer()
    CTmr.Set()
    CJoy = Ojw.CJoystick(nJoy)
    afJoy = [0,0,0,0,0,0]
    while(m_nProgEnd == 0):
        if (m_bInit == False) :
            continue
        CJoy.Update()
        for i in range(0, 10):
            if CJoy.IsDown_Event(i) == True:
                print("Down:" + str(i))
                if i == 7: # Button (Back)
                    m_nProgEnd = 1
        for i in range(0, 6):
            afJoy[i] = round((CJoy.GetPos(i) - 0.5) * 2, 1)
        # if (CTmr.Get() > 1000): # 1초에 한번 확인
        #     CTmr.Set()
        #     print(afJoy[0], afJoy[1], afJoy[2], afJoy[3], afJoy[4], afJoy[5])

        if (CTmr.Get() >= 50): # 100 ms에 한번 확인
            CTmr.Set()
            fRange = 2.0
            
            # X
            if (abs(afJoy[0]) >= 0.5):
                m_fX += afJoy[0] * fRange
                if (m_fX > 100) : 
                    m_fX = 100
                elif (m_fX < -100) :
                    m_fX = -100
            
            # Y
            if (abs(afJoy[1]) >= 0.5):
                m_fY += afJoy[1] * fRange
                if (m_fY > 100) : 
                    m_fY = 100
                elif (m_fY < -100) :
                    m_fY = -100
            
            # 높이
            if (abs(afJoy[3]) >= 0.5):
                m_fH += afJoy[3] * fRange
                if (m_fH > 300) : 
                    m_fH = 300
                elif (m_fH < 200) :
                    m_fH = 200

            #print(m_fX, m_fY, m_fH)
            m_CMot.Move_Delta(0, m_fX, m_fY, m_fH, 1, 0, True)


        if m_nProgEnd != 0:
            break

nJoyIndex = 1
t = threading.Thread(target = JoyControl, args = (nJoyIndex,))
t.start()

# 통신포트 열어주기
m_CMot.Open(6, 1000000)


# 1, 2번 다이나믹셀의 위치 읽어오기
# m_CMot.SyncRead(1)
# m_CMot.SyncRead(2)
# m_CMot.SyncRead(3)
# m_CMot.SyncRead(4)
m_CMot.SyncRead(1,2,3,4)
print(m_CMot.GetAngle(1), m_CMot.GetAngle(2), m_CMot.GetAngle(3))

# 토크를 넣어준다.
m_CMot.SetTorq(True)



m_CMot.Delta_Clear()
m_CMot.Delta_Add(0, 1, 2, 3, 62.5, 100, 245, 32.5)

m_CMot.Move_Delta(0, m_fX, m_fY, m_fH, 1000)

# for i in range(0,10):
#     print(i)
#     m_CMot.Wait(1000)
Move(50, 50, 200, 1000)
Move(-50, 50, 200, 1000)
Move(-50, -50, 200, 1000)
Move(50, -50, 200, 1000)

Move(50, 50, 250, 1000)
Move(-50, 50, 250, 1000)
Move(-50, -50, 250, 1000)
Move(50, -50, 250, 1000)

Move(50, 50, 300, 1000)
Move(-50, 50, 300, 1000)
Move(-50, -50, 300, 1000)
Move(50, -50, 300, 1000)

Move(0, 0, 300, 1000)

m_bInit = True

while(m_nProgEnd == 0):
    m_CMot.Wait(1000)

# 통신을 닫는다.
m_CMot.Close()