from pymodbus.client.sync import ModbusTcpClient
import time

# 로봇의 IP 주소와 Modbus 포트 설정
robot_ip = '192.168.1.100'  # 두산 로봇의 IP 주소
modbus_port = 502  # Modbus TCP 기본 포트

# Modbus TCP 클라이언트 생성
client = ModbusTcpClient(robot_ip, port=modbus_port)

# 클라이언트 연결
if client.connect():
    print("Connected to the robot")

    # 주기적으로 레지스터 폴링
    while True:
        # 예제: 디지털 입력 레지스터 (주소 0부터 1개 레지스터 읽기)
        result = client.read_discrete_inputs(0, 1)
        if result.isError():
            print("Error reading discrete inputs")
        else:
            # 상태 확인
            status = result.bits[0]
            print(f"Discrete input status: {status}")

            # 상태 변화에 따른 처리
            if status:
                # 상태가 1이면 (예: 이벤트 발생) 처리 로직 수행
                print("Event detected, processing...")
                # 필요 시 다른 명령 실행

        # 주기적 폴링을 위한 대기 (1초 대기)
        time.sleep(1)

    # 클라이언트 연결 종료
    client.close()
    print("Connection closed")
else:
    print("Unable to connect to the robot")
