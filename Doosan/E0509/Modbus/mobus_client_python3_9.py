
from pymodbus.client import ModbusTcpClient
import time

# 로봇의 IP 주소와 Modbus 포트 설정
robot_ip = '192.168.137.100'  # 두산 로봇의 IP 주소
modbus_port = 502  # Modbus TCP 기본 포트

# Modbus TCP 클라이언트 생성
client = ModbusTcpClient(robot_ip, port=modbus_port)


# 로봇 상태 리스트 및 다음 행동 목록
robot_action_dic = {'robot_off' : {
                        'current_state' : [0,0,0,0,0],
                        'next_action' : ['power_on', [0, True]]
                        },
                    'robot_on' : {
                        'current_state' : [3,0,0,0,0],
                        'next_action' : ['script_start',[1,False]]
                        },
                    'robot_running' : {
                        'current_state' : [3,1,1,0,0],
                        'next_action' : ['manual_on',[2,True]]
                        },
                    'ss2' : {
                        'current_state' : [5,3,3,0,0],
                        'next_action' : ['error_off',[3,False]]
                        }
                    }

# 로봇의 현재 상태 체크 ( read_holding_register )
def check_robot():
    current_state_dic = [list(format(client.read_holding_registers(1, 1, 1).registers[0], '016b'))[::-1], # "digital_output"
                        list(format(client.read_holding_registers(0, 1, 1).registers[0], '016b'))[::-1], #"digital_input"
                        client.read_holding_registers(259, 1, 1).registers[0], #"robot_state"
                        client.read_holding_registers(260, 1, 1).registers[0], #"servo_on_robot"
                        client.read_holding_registers(261, 1, 1).registers[0], #"emergency_stopped"
                        client.read_holding_registers(262, 1, 1).registers[0], #"safety_stopped"
                        client.read_holding_registers(263, 1, 1).registers[0], #"direct_teach_button_pressed"
                        client.read_holding_registers(264, 1, 1).registers[0] #"power_button_pressed"
                        ]
    current_state_arr = []
    for a in current_state_dic:
        current_state_arr.add(a)
    return current_state_arr

# 로봇의 상태 변경 ( write_coil )
def write_coil(robot_action_dic, robot_state):
    print(f'current state = {robot_state}\ncommand action : {robot_action_dic[robot_state]["next_action"][0]}')
    try:
        write_coil = robot_action_dic[robot_state]['next_action'][1]
        client.write_coil(write_coil)
        return True
    except:
        return False

# 로봇의 현 상태 확인 후 until_state까지 상태 변경
def action_robot2(robot_action_dic, until_state):

    while True:
        target_state = check_robot()
        matching_keys = [key for key, value in robot_action_dic.items() if value['current_state'] == target_state]
        robot_state = ''
        for key in matching_keys:
            robot_state = key
        if robot_state == until_state:
            break
        else:
            # case문을 통해 본인의 state부터 순차 실행
            match robot_state:
                case 'ss2':
                    pass
                case 'robot_off':
                    write_coil(robot_action_dic,robot_state)
                case 'robot_on':
                    pass
                case 'servo_on':
                    pass

        return 'robot ready'

action_robot2(robot_action_dic,'robot_running')
