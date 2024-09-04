from pprint import pprint
from pymodbus.client import ModbusTcpClient
import time

# 로봇의 IP 주소와 Modbus 포트 설정
robot_ip = '192.168.137.100'  # 두산 로봇의 IP 주소
modbus_port = 502  # Modbus TCP 기본 포트

# Modbus TCP 클라이언트 생성
client = ModbusTcpClient(robot_ip, port=modbus_port)


#wclient.connect()
# 클라이언트 연결
# if client.connect():
#     print("Connected to the robot")


#     # ---------------------------coil-----------------------------------
#     # Coil (디지털 출력) 제어 예제: 1번 핀을 HIGH로 설정
#     coil_address = 129  # 제어할 Coil의 주소
#     value = True  # HIGH로 설정

#     # # Coil 제어 (쓰기)
#     # result = client.write_coil(coil_address, True)
#     # if result.isError():
#     #    print("Error writing to coil")
#     # else:
#     #    print(f"Successfully wrote to coil {coil_address}, {result}")

#     # # Coil 읽기 (확인)
#     # result = client.read_coils(coil_address, 1)
#     # if result.isError():
#     #     print("Error reading coil")
#     # else:
#     #     print(f"Coil {coil_address} value: {result} {result.bits[0]}")
#     # # -------------------------------------------------------------------------------

#     # Holding Register
#     result = client.read_holding_registers(259,1,1)
#     if result.isError():
#         print("Error writing to holding register")
#     else:
#         print(f"Successfully wrote to holding register : {result.registers}")

#     result = client.read_holding_registers(1)
#     if result.isError():
#         print("Error writing to holding register")
#     else:
#         print(f"Successfully wrote to holding register : {result.registers}")
#         print(f"Successfully digital output 1~16 : {bin(result.registers[0])}")
#         a=format(result.registers[0],'016b')
#         print(f"Successfully digital output 1~16 : {a}")

#     '''
#     result = client.write_registers(1)
#     if result.isError():
#         print("Error writing to holding register")
#     else:
#         print(f"Successfully wrote to holding register : {result}")
#     '''

#     # 클라이언트 연결
#     client.close()
#     print("Connection closed")
# else:
#     print("Unable to connect to the robot")

#---------remote mode on------------
#result = client.write_coil(16,True)
#result = client.write_coil(17,True)


#--------power on -> servo on -> task ready------------
# result = client.write_coil(24,True)
# result = client.write_coil(25,True)
# result = client.write_coil(20,True)

#--------task ready -> task run------------------
# client.write_coil(22, True)
# client.write_coil(21, False)
# time.sleep(2)
# client.write_coil(21, True)

#------



#result = client.write_coil(18,False)
#result = client.write_coil(20,False)
# print(result.isError())
# print(list(format(client.read_holding_registers(1,1,1).registers[0],'016b'))[::-1])


client.write_coil(24, False)
client.write_coil(25, False)
time.sleep(2)
client.write_coil(16, False)
client.write_coil(17, False)
client.write_coil(20, False)
# result = client.write_coil(20,True)
# print(list(format(client.read_holding_registers(1,1,1).registers[0],'016b'))[::-1])

#client.write_coil(21,True)
#client.write_coil(19,True)

time.sleep(2)

if client.connect():
    robot_state = {
        "controlbox_state" : {
            "digital_output" : list(format(client.read_holding_registers(1,1,1).registers[0],'016b'))[::-1],
            "digital_input" : list(format(client.read_holding_registers(0,1,1).registers[0],'016b'))[::-1],
            "robot_state" : client.read_holding_registers(259,1,1).registers[0],
            "servo_on_robot" : client.read_holding_registers(260,1,1).registers[0],
            "emergency_stopped" : client.read_holding_registers(261,1,1).registers[0],
            "safety_stopped" : client.read_holding_registers(262,1,1).registers[0],
            "direct_teach_button_pressed" : client.read_holding_registers(263,1,1).registers[0],
            "power_button_pressed" : client.read_holding_registers(264,1,1).registers[0]
        }

    }
    pprint(robot_state)
    time.sleep(1)
    