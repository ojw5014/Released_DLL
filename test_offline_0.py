# pip install pythonnet 으로 설치
import clr
clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw

COjw = Ojw()
m_CMot = Ojw.CProtocol2()
# 통신포트 열어주기
m_CMot.Open(26, 1000000)


# 1, 2번 다이나믹셀의 위치 읽어오기
m_CMot.SyncRead(1,2,3,4,5,6,7)

# 토크를 넣어준다.
m_CMot.SetTorq(True)
# 1, 2번 다이나믹셀을 둘다 90도 위치로 변경
m_CMot.PlayFrameString("S2,5000,0,1:90,2:90,3:90")
#m_CMot.Wait(3000)

# 위치를 0으로 변경
m_CMot.PlayFrameString("S2,1000,0,2:0,1:0,3:30")
#m_CMot.Wait(3000)


# 1, 2번 다이나믹셀을 둘다 90도 위치로 변경
m_CMot.PlayFrameString("S2,1000,0,1:90,2:90,3:90")

# 위치를 0으로 변경
m_CMot.PlayFrameString("S2,1000,0,2:0,1:-30,3:30")

# PC의 Comport를 체크한다.
#strPorts = Ojw.CSerial.GetPortNames()
#for strPort in strPorts:
#    print(strPort)
anPorts = Ojw.CSerial.GetPorts()
for nPort in anPorts:
    print(nPort)


# 통신을 닫는다.
m_CMot.Close()