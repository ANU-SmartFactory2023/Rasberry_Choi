# py3.py
import random
import os
import sys
import time
import RPi.GPIO as GPIO


# 현재 스크립트 파일의 디렉토리 경로
current_path = os.path.dirname(__file__)
# 외부 폴더의 경로 지정 (예: /home/pi/external_folder)
external_path = os.path.join(current_path, '/home/admin3/test/common')
# sys.path에 외부 폴더 경로 추가
sys.path.append(external_path)

from enum import Enum
# 모듈 또는 파일 불러오기# py3.py
import random
import os
import sys
import time
import RPi.GPIO as GPIO


# 현재 스크립트 파일의 디렉토리 경로
current_path = os.path.dirname(__file__)
# 외부 폴더의 경로 지정 (예: /home/pi/external_folder)
external_path = os.path.join(current_path, '/home/admin3/test/common')
# sys.path에 외부 폴더 경로 추가
sys.path.append(external_path)

from enum import Enum
# 모듈 또는 파일 불러오기
from server_communication import ServerComm
from sensor import Sensor
from motor import Motor, GuideMotorStep



class Step( Enum ) :
    start=0    
    second_part_irsensor_check = 10 
    third_part_irsensor_check = 20
    go_rail= 30 
    stop_rail = 40
    third_part_irsensor_post = 50
    third_part_process_start = 60
    third_part_process_sleep = 70
    third_part_sensor_measure = 80
    third_part_process_end = 90
    servo = 100
   
pass_or_fail = ''

SERVO_PIN = 16
SECOND_PART_SENSOR_PIN_NO = 17
THIRD_PART_SENSOR_PIN_NO = 18
    

currnet_step = Step.start
running = True

sensor = Sensor()
servercomm = ServerComm()
motor = Motor(servo_pin)


while running:
    print( "running : " + str( running ) )# 디버깅확인용
    time.sleep( 0.1 )
    THIRD_IR = sensor.get_ir_sensor( THIRD_PART_SENSOR_PIN_NO )
    RELAY
    match currnet_step :
        case Step.start: 
            print( Step.start )
            motor.doGuideMotor( GuideMotorStep.stop )
            #시작하기전에 검사할것들: 통신확인여부, 모터정렬, 센서 검수
            currnet_step = Step.second_part_irsensor_check
        
        case Step.second_part_irsensor_check:
            print( Step.second_part_irsensor_check )
            if( sensor.get_ir_sensor( SECOND_PART_SENSOR_PIN_NO )==0 ):
                # 2차 공정 두 번째 적외선 센서 값이 0이면
                current_step = Step.go_rail
            else:
                
        # 두 번째 컨베이어 벨트 구동
        case Step.go_rail:
            print( Step.go_rail )
            motor.doConveyor();           
            currnet_step = third_part_irsensor_check

        case Step.third_part_irsensor_check:
            print( Step.third_part_irsensor_check )
            if( THIRD_IR == 1 ):
                # 이온주입 공정 적외선 센서 값이 1인 상태
                # 컨베이어 벨트 정지
                currnet_step = stop_rail 
            else:             
                # 이온주입 공정 적외선 센서 값이 0인 상태 
                print("제품 도착 전")
                currnet_step = Step.third_part_irsensor_check

        case Step.stop_rail:
            # 적외선 센서 감지로 컨베이어벨트 중단
            print( Step.stop_rail )
            motor.stopConveyor()
            currnet_step = Step.third_part_irsensor_post

        case Step.third_part_irsensor_post:
            print( third_part_irsensor_post )
            # 서버에게 적외선 센서 감지 여부 전송
            decect_reply = confirmationObject(3, THIRD_IR)

            # 답변 중 msg 변수에 "ok" 를 확인할 시
            if( detect_reply == "ok"):
                current_step = Step.third_part_process_start
            else:
                current_step = Step.third_part_irsensor_post

        case Step.third_part_process_start:
            print( third_part_process_start )
            start_reply = ionlmplantationStart()

            # 제조 시작을 알리는 ionlmplantationStart() 함수 호출
            # 답변 중 msg 변수에 "ok" 를 확인할 시
            if( start_reply == "ok"):
                current_step = Step.third_part_process_sleep
            else:
                current_step = Step.third_part_process_start

        case Step.third_part_process_sleep:
            # 랜덤값 변수 대입 후 딜레이 (제조 시간 구현)
            print( Step.third_part_process_sleep )
            random_time = random.randint(4, 8)
            sleep(random_time)

            # 딜레이(제조)가 다 끝나면
            current_step = Step.third_part_sensor_measure

        # 3차 공정 품질 검사 센서값 추출
        case Step.third_part_sensor_measure_and_endpost:
            print( Step.third_part_sensor_measure )
            # 릴레이 모듈 값을 전도성 판단
            relay_value = sensor.get_relay_sensor()
            # 릴레이 모듈 값을 서버에 전송
            end_reply = ionlmplantationEnd(relay_value)

            # 답변 따라 GuideMotorStep(good or fail) 클래스 Enum 설정
            if(end_reply = "pass"):
                pass_or_fail = good
            else:
                pass_or_fail = fail

            current_step = Step.servo

##########################################################################
        # doGuideMotor(GuideMotorStep) 함수를 호출하여 서보모터 작동
        case Step.servo:
            print( Step.servo )






                
            

               
            #     motor.doConveyor()
                
            #     # 세 번째 공정 ir 센서 값에 따라 통신 과정 이동
            #     if(THIRD_IR==1):
            #         motor.stopConveyor()
            #         currnet_step = Step.ionlmplantation_process_POST
            #     else:
            #         motor.doConveyor()
            # else: 
            #     motor.stopConveyor()

                
            
        case Step.ionlmplantation_process_POST:
            print( Step.ionlmplantation_process_POST )
            # 제조 공정 시작 전 3차 공정 적외선 감지 POST
            result = servercomm.confirmationObject(3, THIRD_IR)
            
            if( result == "ok" ):
                currnet_step = Step.go_rail          
            else:
                currnet_step = Step.ionlmplantation_process_POST

            
        case Step.go_rail:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.end

        case Step.photo_part_detect_sensor_check:
            print( Step.photo_part_detect_sensor_check )
            if( sensor.get_sensor_state(PHOTO_PART_SENSOR_PIN_NO) ):                
                currnet_step = Step.stop_rail

        case Step.stop_rail:
            print( Step.stop_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.photo_process
        
        case Step.photo_process:
            print( Step.photo_process)
            result = sensor.#이미지 처리 값
            pass_or_fail = server_comm.#서버에값을 전달( result )

            currnet_step = Step.servo_motor_drive
                
        case Step.servo_motor_drive:
            motor_step = GuideMotorStep.stop
            if( pass_or_fail ):
                motor_step = GuideMotorStep.good
            else :
                motor_step = GuideMotorStep.fail

            motor.doGuideMotor( motor_step )

        case Step.go_rail_next:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.end
            
        case Step.sonic_part_detect_sensor_check:
            print( Step.sonic_part_detect_sensor_check )
            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO) ):                
                currnet_step = Step.slow_rail

        case Step.slow_rail:
            print( Step.slow_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.start
from server_communication import ServerComm
from sensor import Sensor
from motor import Motor, GuideMotorStep



class Step( Enum ) :
    start=0    
    irsensor_check = 10  
    ionlmplantation_process_POST = 50

    ############################# 
    wait_server_state = 20 
    go_rail= 30        
    
    stop_rail = 100
    photo_process = 150
    servo_motor_drive =300  
    sonic_part_detect_sensor_check= 400
    slow_rail = 500

    
pass_or_fail:bool = False

SERVO_PIN = 16
SECOND_PART_SENSOR_PIN_NO = 17
THIRD_PART_SENSOR2_PIN_NO = 18
    

currnet_step = Step.start
running = True

sensor = Sensor()
servercomm = ServerComm()
motor = Motor(servo_pin)


while running:
    print( "running : " + str( running ) )# 디버깅확인용
    time.sleep( 0.1 )
    THIRD_IR = sensor.get_ir_sensor( THIRD_PART_SENSOR2_PIN_NO )
    match currnet_step :
        case Step.start: 
            print( Step.start )
            motor.doGuideMotor( GuideMotorStep.stop )
            #시작하기전에 검사할것들: 통신확인여부, 모터정렬, 센서 검수
            currnet_step = Step.second_irsensor_check
        
        case Step.second_irsensor_check:
            print( Step.irsensor_check )
            if( sensor.get_ir_sensor( SECOND_PART_SENSOR_PIN_NO )==0 ):
                # 전 공정 적외선 센서 값이 0인 상태               
                motor.doConveyor()
                
                # 세 번째 공정 ir 센서 값에 따라 통신 과정 이동
                if(THIRD_IR==1):
                    motor.stopConveyor()
                    currnet_step = Step.ionlmplantation_process_POST
                else:
                    motor.doConveyor()
            else: 
                motor.stopConveyor()

                
            
        case Step.ionlmplantation_process_POST:
            print( Step.ionlmplantation_process_POST )
            # 제조 공정 시작 전 3차 공정 적외선 감지 POST
            result = servercomm.confirmationObject(3, THIRD_IR)
            ##############################################
            if( result == "ok" ):
                currnet_step = Step.go_rail
            
        case Step.go_rail:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.end

        case Step.photo_part_detect_sensor_check:
            print( Step.photo_part_detect_sensor_check )
            if( sensor.get_sensor_state(PHOTO_PART_SENSOR_PIN_NO) ):                
                currnet_step = Step.stop_rail

        case Step.stop_rail:
            print( Step.stop_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.photo_process
        
        case Step.photo_process:
            print( Step.photo_process)
            result = sensor.#이미지 처리 값
            pass_or_fail = server_comm.#서버에값을 전달( result )

            currnet_step = Step.servo_motor_drive
                
        case Step.servo_motor_drive:
            motor_step = GuideMotorStep.stop
            if( pass_or_fail ):
                motor_step = GuideMotorStep.good
            else :
                motor_step = GuideMotorStep.fail

            motor.doGuideMotor( motor_step )

        case Step.go_rail_next:
            print( Step.go_rail )
            result = motor.#DC모터 구동            
            currnet_step = Step.end
            
        case Step.sonic_part_detect_sensor_check:
            print( Step.sonic_part_detect_sensor_check )
            if( sensor.get_sensor_state(SONIC_PART_SENSOR_PIN_NO) ):                
                currnet_step = Step.slow_rail

        case Step.slow_rail:
            print( Step.slow_rail )
            result = motor.#DC모터 정지            
            currnet_step = Step.start