import clr
clr.AddReference("OpenJigWare")
from OpenJigWare import Ojw
COjw = Ojw()
m_CMot = Ojw.CProtocol2()
# 통신포트 열어주기
m_CMot.Open(3, 1000000)

# 토크를 넣어준다.
m_CMot.SetTorq(True)

# 1, 2번 다이나믹셀의 위치 읽어오기
m_CMot.SyncRead(1,2,3,4,5,6,7)



# m_CMot.PlayFrameString("S2,1000,0,1:90,2:90")

# m_CMot.PlayFrameString('S2,2000,0,1:30')
# m_CMot.Wait()
m_CMot.PlayFrameString('S2,5000,0,1:30,2:0,3:0,4:0,5:0,6:0,7:0')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,5000,0,2:90,3:130,4:50,5:90,6:0')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,2000,0,6:90')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,2000,0,7:60')
m_CMot.Wait()
m_CMot.Wait(2000)
m_CMot.PlayFrameString('S2,2000,0,7:0')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,2000,0,6:0')
m_CMot.Wait()
m_CMot.PlayFrameString('S2,2000,0,2:0,3:0,4:0,5:0,6:0')
m_CMot.Wait()
# m_CMot.PlayFrameString('S2,10000,0,12:-20, 13:20, 14:-20')
# m_CMot.Wait()
# m_CMot.PlayFrameString('S2,10000,0,12:-30, 13:30, 14:-10')
# m_CMot.Wait()
# m_CMot.PlayFrameString('S2,10000,0,12:-40,13:40,14:-20')
# m_CMot.Wait()
# m_CMot.PlayFrameString('S2,10000,0,12:-50,13:50,14:-30')
# m_CMot.Wait()
# m_CMot.PlayFrameString('S2,1000,0,12:0,13:0,14:0')
# m_CMot.Wait()


# m_CMot.PlayFrameString('S2,1000,0,15:-60,')
# m_CMot.Wait()
# m_CMot.PlayFrameString('S2,1000,0,15:0,')


m_CMot.PlayFrameString('S2,5000,0,1:0')
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
