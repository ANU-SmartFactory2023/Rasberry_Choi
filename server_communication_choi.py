#server_communication.py
import http.client
import json
from models import Process

# 클래스의 메서드에서 첫 번째 매개변수로 self를 사용하는 것은 파이썬의 규칙 중 하나입니다. 
# self를 사용하여 클래스의 인스턴스 변수 및 메서드에 접근할 수 있습니다.
class ServerComm :
    conn:http.client.HTTPConnection
    headers = {"Content-type": "application/json", "Accept": "*/*"}
    
    def __init__( self ) :
        self.conn = http.client.HTTPConnection( 'localhost', 5294 )

    # HTTP 통신 Post 정의
    def requestPost( self, url, p:Process ) :
        self.conn.request( 'POST', url, json.dumps( p.__dict__ ), self.headers )
        result = self.conn.getresponse().read().decode()
        json_object = json.loads( result )

        return json_object

    # HTTP 통신 Get 정의
    def requestGet( self, url ) :
        self.conn.request( 'GET', url  )
        result = self.conn.getresponse().read().decode()
        json_object = json.loads( result )

        return json_object
    
    # 공정 시작 전 제품 도착 여부 전송 (Get)
    def ready(self) :
        json_object = self.requestGet( '/api/sensor/0' )

        msg = json_object[ 'msg' ]
        if msg == 'ok':
            return True
        else:
            return False

    # 1~4 차 제조 공정 전 제품 도착 여부 전송 (Post)
    def confirmationObject( self, idx, on_off ) :
        p = Process.SensorModel()
        
        p.sensorName = "detect"
        p.sensorState = on_off

        res = self.requestPost( f'/pi/sensor/{idx}', p )

        return res
    
    # 각 공정마다 인수를 넣지 않고 간단하게 호출할 수 있도록
    # 공정마다 매개변수를 통신 클래스에서 먼저 정의하는 방법
    def photoStart( self ):
        self.__checkProcess( 1, "start", "photo", "0")

    def photoEnd( self, processValue):
        self.__checkProcess( 1, "end", "photo", processValue)

    #이 뒤로 2, 3, 4 공정 start, end 추가 예정
    

    # 1~4 차 제조 공정 후 불량품 구분을 위한 센서값 전송 (Post)
    def __checkProcess( self, idx, processCmd, processName, processValue):
        p = Process.ProcessModel()
        p.processCmd = processCmd
        p.processName = processName
        p.processValue = processValue

        res = self.request_post( f'/pi/process/{idx}', p )

        return res
    
    #def scheduler( self, idx, )











    def send_data(self, p:Process, path: str = '/api/Process') :
        self.conn.request( 'POST', path, json.dumps( p.__dict__ ), self.headers )
        result = self.conn.getresponse().read().decode()
        
        print( "recvdata : " + result )