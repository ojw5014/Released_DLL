import clr

# DLL의 경로를 sys.path에 추가
# import sys
# sys.path.append('d:\\Bin\\cs\\OpenJigWare\\trunk\\Released_DLL')


clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw
COjw = Ojw()

print(COjw.__version__)
m_CMot = Ojw.CProtocol2()
# 통신포트 열어주기
m_CMot.Open(3, 1000000)

# 토크를 넣어준다.
m_CMot.SetTorq(True)

# 1, 2번 다이나믹셀의 위치 읽어오기
# m_CMot.SyncRead(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
m_CMot.SyncRead(1,2,3)
# Ojw.CTimer.Wait(3000)
strData = ""
# for i in range(0,17):
for i in range(0,3):
    print(i + 1)
    strData = strData + Ojw.CConvert.FloatToStr(m_CMot.GetAngle(i + 1)) + ", "
# print("Down:" + Ojw.CConvert.FloatToStr(m_CMot.GetAngle(1)) + ", " + Ojw.CConvert.FloatToStr(m_CMot.GetAngle(2)) + ", " + Ojw.CConvert.FloatToStr(m_CMot.GetAngle(3)))
print(strData)
#m_CMot.PlayFrameString("S2,1000,0,1:0,2:0,3:0")
m_CMot.Close()
exit()


# 1, 2번 다이나믹셀을 둘다 90도 위치로 변경
m_CMot.PlayFrameString("S2,1000,0,1:90,2:90,")
m_CMot.Wait()

# 위치를 0으로 변경
m_CMot.PlayFrameString("S2,1000,0,2:0,1:0,")
m_CMot.Wait()

# PC의 Comport를 체크한다.
#strPorts = Ojw.CSerial.GetPortNames()
#for strPort in strPorts:
#    print(strPort)
anPorts = Ojw.CSerial.GetPorts()
for nPort in anPorts:
    print(nPort)


# 통신을 닫는다.
m_CMot.Close()

# DLL의 경로를 sys.path에 추가
# import sys
# sys.path.append('d:\\Bin\\cs\\OpenJigWare\\trunk\\Released_DLL')

m_CMon = Ojw.CMonster2()
m_CMon.Open(25, 1000000)

m_CMon.SetTorq(True)

m_CMon.Set(1, -90)
m_CMon.Set(2, -90)
m_CMon.SetLed(1, 1)
m_CMon.SetLed(2, 1)
m_CMon.Send_Motor(1000)
m_CMon.Wait(1000)


m_CMon.Set(1, 0)
m_CMon.Set(2, 0)
m_CMon.SetLed(1, 0)
m_CMon.SetLed(2, 0)
m_CMon.Send_Motor(1000)
m_CMon.Wait(1000)


m_CMon.SetLed(1, 1)
m_CMon.SetLed(2, 1)
m_CMon.Wait(1000)

m_CMon.SetLed(1, 0)
m_CMon.SetLed(2, 0)
m_CMon.Wait(1000)

m_CMon.SetLed(1, 1)
m_CMon.SetLed(2, 1)
m_CMon.Wait(1000)

m_CMon.SetLed(1, 0)
m_CMon.SetLed(2, 0)
m_CMon.Wait(1000)

nCnt = 0
CJoy = Ojw.CJoystick(1)
while(True):
    CJoy.Update()
    for i in range(0, 10):
        if CJoy.IsDown_Event(i) == True:
            nCnt = nCnt + 1
            print("Down:")# + str(i))
            if nCnt > 3:
                break
    if nCnt > 3:
        break

m_CMon.Close()