from pprint import pprint
from pymodbus.client import ModbusTcpClient

# 로봇의 IP 주소와 Modbus 포트 설정
robot_ip = '192.168.1.101'  # 두산 로봇의 IP 주소
modbus_port = 502  # Modbus TCP 기본 포트

# Modbus TCP 클라이언트 생성
client = ModbusTcpClient(robot_ip, port=modbus_port)



# 클라이언트 연결
if client.connect():
    print("Connected to the robot")


    # ---------------------------coil-----------------------------------
    # Coil (디지털 출력) 제어 예제: 1번 핀을 HIGH로 설정
    coil_address = 23  # 제어할 Coil의 주소
    value = True  # HIGH로 설정

    # Coil 제어 (쓰기)
    result = client.write_coil(coil_address, True)
    if result.isError():
        print("Error writing to coil")
    else:
        print(f"Successfully wrote to coil {coil_address}, {result}")

    # Coil 읽기 (확인)
    result = client.read_coils(coil_address, 1)
    if result.isError():
        print("Error reading coil")
    else:
        print(f"Coil {coil_address} value: {result} {result.bits[0]}")
    # -------------------------------------------------------------------------------

    # Holding Register
    result = client.read_holding_registers(259)
    if result.isError():
        print("Error writing to holding register")
    else:
        print(f"Successfully wrote to holding register : {result.registers}")

    result = client.read_holding_registers(1)
    if result.isError():
        print("Error writing to holding register")
    else:
        print(f"Successfully wrote to holding register : {result.registers}")
        print(f"Successfully digital output 1~16 : {bin(result.registers[0])}")
        a=format(result.registers[0],'016b')
        print(f"Successfully digital output 1~16 : {a}")

    '''
    result = client.write_registers(1)
    if result.isError():
        print("Error writing to holding register")
    else:
        print(f"Successfully wrote to holding register : {result}")
    '''

    # 클라이언트 연결 종료
    client.close()
    print("Connection closed")
else:
    print("Unable to connect to the robot")

robot_state = {
    "controlbox_state" : {
        "digital_output" : list(format(client.read_holding_registers(1).registers[0],'016b'))[::-1],
        "digital_input" : list(format(client.read_holding_registers(0).registers[0],'016b'))[::-1],
        "servo_on_robot" : client.read_holding_registers(260).registers[0],
        "emergency_stopped" : client.read_holding_registers(261).registers[0],
        "safety_stopped" : client.read_holding_registers(262).registers[0],
        "direct_teach_button_pressed" : client.read_holding_registers(263).registers[0],
        "power_button_pressed" : client.read_holding_registers(264).registers[0]
    },
    
    "arm_state" : {
        "joint_position" : [
            client.read_holding_registers(270).registers[0],
            client.read_holding_registers(271).registers[0],
            client.read_holding_registers(272).registers[0],
            client.read_holding_registers(273).registers[0],
            client.read_holding_registers(274).registers[0],
            client.read_holding_registers(275).registers[0]
            ],
        "joint_velocity" : [
            client.read_holding_registers(280).registers[0],
            client.read_holding_registers(281).registers[0],
            client.read_holding_registers(282).registers[0],
            client.read_holding_registers(283).registers[0],
            client.read_holding_registers(284).registers[0],
            client.read_holding_registers(285).registers[0]
            ],
        "joint_motor_current" : [
            client.read_holding_registers(290).registers[0],
            client.read_holding_registers(291).registers[0],
            client.read_holding_registers(292).registers[0],
            client.read_holding_registers(293).registers[0],
            client.read_holding_registers(294).registers[0],
            client.read_holding_registers(295).registers[0]
            ],
        "joint_motor_tempuature" : [
            client.read_holding_registers(300).registers[0],
            client.read_holding_registers(301).registers[0],
            client.read_holding_registers(302).registers[0],
            client.read_holding_registers(303).registers[0],
            client.read_holding_registers(304).registers[0],
            client.read_holding_registers(305).registers[0]
            ],
        "joint torque" : [
            client.read_holding_registers(310).registers[0],
            client.read_holding_registers(311).registers[0],
            client.read_holding_registers(312).registers[0],
            client.read_holding_registers(313).registers[0],
            client.read_holding_registers(314).registers[0],
            client.read_holding_registers(315).registers[0]
            ]
        
    }

}
pprint(robot_state)

def robot_init():
    check = client.read_coil (coil_address, 1)
    if check.isError():
        return -1
    else :
        result = client.write_coil(coil_address)
        if True:
            pass


# 클라이언트 연결
if client.connect():
    print("Connected to the robot")


    # ---------------------------coil-----------------------------------
    # Coil (디지털 출력) 제어 예제: 1번 핀을 HIGH로 설정
    coil_address = 23  # 제어할 Coil의 주소
    value = True  # HIGH로 설정

    # Coil 제어 (쓰기)
    result = client.write_coil(coil_address, True)
    if result.isError():
        print("Error writing to coil")
    else:
        print(f"Successfully wrote to coil {coil_address}, {result}")

    # Coil 읽기 (확인)
    result = client.read_coils(coil_address, 1)
    if result.isError():
        print("Error reading coil")
    else:
        print(f"Coil {coil_address} value: {result} {result.bits[0]}")
    # -------------------------------------------------------------------------------

    # Holding Register
    result = client.read_holding_registers(259)
    if result.isError():
        print("Error writing to holding register")
    else:
        print(f"Successfully wrote to holding register : {result.registers}")

    result = client.read_holding_registers(1)
    if result.isError():
        print("Error writing to holding register")
    else:
        print(f"Successfully wrote to holding register : {result.registers}")
        print(f"Successfully digital output 1~16 : {bin(result.registers[0])}")
        a=format(result.registers[0],'016b')
        print(f"Successfully digital output 1~16 : {a}")

    # rsult = client.write_registers(1)
    # if result.isError():
    #     print("Error writing to holding register")
    # else:
    #     print(f"Successfully wrote to holding register : {result}")

    # 클라이언트 연결 종료
    client.close()
    print("Connection closed")
else:
    print("Unable to connect to the robot")

