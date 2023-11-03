import clr

# DLL의 경로를 sys.path에 추가
import sys
#sys.path.append('d:\\Bin\\cs\\OpenJigWare\\trunk\\Released_DLL')
clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw
COjw = Ojw()
#result = Ojw.CConvert.IntToHex(64)
#print(result)

m_CMot = Ojw.CProtocol2()
# 통신포트 열어주기
m_CMot.Open(6, 1000000)

# 토크를 넣어준다.
m_CMot.SetTorq(True)

# 1, 2번 다이나믹셀의 위치 읽어오기
m_CMot.SyncRead(11,12,13,14,15)



# m_CMot.PlayFrameString("S2,1000,0,1:90,2:90")

m_CMot.PlayFrameString('S2,1000,0,11:30')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,12:-10, 13:10, 14:-30')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,12:-20, 13:20, 14:-20')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,12:-30, 13:30, 14:-10')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,12:-40,13:40,14:-20')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,12:-50,13:50,14:-30')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,12:0,13:0,14:0')
m_CMot.Wait()


m_CMot.PlayFrameString('S2,1000,0,15:-60,')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,1000,0,15:0,')


m_CMot.PlayFrameString('S2,1000,0,11:0')
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
