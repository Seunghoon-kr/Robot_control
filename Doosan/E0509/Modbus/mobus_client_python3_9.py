from pymodbus.client import ModbusTcpClient
import time

# 로봇의 IP 주소와 Modbus 포트 설정
robot_ip = '192.168.137.100'  # 두산 로봇의 IP 주소
modbus_port = 502            # Modbus TCP 기본 포트


class ModbusMaster:
    def __init__(self):
        """Modbus TCP 클라이언트 초기화"""
        self.client = ModbusTcpClient(robot_ip, port=modbus_port)

    def check_robot(self):
        """로봇의 현재 상태 체크 (read_holding_register)"""
        time.sleep(0.5)
        try:
            dio_list = self.client.read_holding_registers(0).registers[0]
            current_state = list(map(int, format(dio_list, '016b')))[::-1]  # 16비트 -> 리스트 변환
            current_state.extend([
                self.client.read_holding_registers(259).registers[0],
                self.client.read_holding_registers(260).registers[0],
                self.client.read_holding_registers(261).registers[0],
                self.client.read_holding_registers(262).registers[0],
                self.client.read_holding_registers(263).registers[0],
                self.client.read_holding_registers(264).registers[0]
            ])
            print(f"현재 상태: {current_state}")
            return current_state
        except Exception as e:
            print(f"상태 확인 오류: {e}")
            return []

    def write_coil(self, address, value):
        """Modbus Coil 쓰기 (write_coil)"""
        try:
            self.client.write_coil(address, value)
            print(f"Coil {address}에 {value} 값 쓰기 성공")
            return True
        except Exception as e:
            print(f"Coil 쓰기 실패: {e}")
            return False

    def wait_for_state(self, expected_state, timeout=5):
        """특정 상태까지 대기"""
        cnt = 0
        while cnt < timeout:
            current_state = self.check_robot()
            if current_state == expected_state:
                print("목표 상태 도달")
                return True
            time.sleep(2)
            cnt += 1
        print("대기 시간 초과")
        return False

    def main(self):
        """메인 실행 함수"""
        count = 0
        try:
            while True:
                count += 1
                print(f"\n===== 반복 횟수: {count} =====")
                robot_state = self.check_robot()
                time.sleep(2)

                match robot_state:
                    case [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 3, 0, 0, 0, 0, 0]:
                        print("완료 : 로봇 부팅 완료")
                        print("시도 : 원격 제어 설정")
                        self.write_coil(16, True)
                        self.write_coil(17, True)
                        self.wait_for_state([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 3, 0, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 3, 0, 0, 0, 0, 0]:
                        print("완료 : 원격 제어 설정 완료")
                        print("시도 : 로봇 서보 온")
                        self.write_coil(20, False)
                        time.sleep(2)
                        self.write_coil(20, True)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 3, 0, 0, 0, 0, 0]:
                        print("완료 : 원격 제어 설정 완료")
                        print("시도 : 로봇 서보 온")
                        self.write_coil(20, False)
                        time.sleep(2)
                        self.write_coil(20, True)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]:
                        print("완료 : 로봇 서보 온 완료")
                        print("시도 : 로봇 스크립트 시작")
                        self.write_coil(21, False)
                        self.write_coil(22, True)
                        self.write_coil(23, True)
                        time.sleep(1)
                        self.write_coil(21, True)
                        self.wait_for_state([1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 16, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]:
                        print("완료 : 로봇 서보 온 완료")
                        print("시도 : 로봇 스크립트 시작")
                        self.write_coil(21, False)
                        self.write_coil(22, True)
                        self.write_coil(23, True)
                        time.sleep(1)
                        self.write_coil(21, True)
                        self.wait_for_state([1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 16, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]:
                        print("완료 : 로봇 서보 온 완료")
                        print("시도 : 로봇 스크립트 시작")
                        self.write_coil(21, False)
                        self.write_coil(22, True)
                        self.write_coil(23, True)
                        time.sleep(1)
                        self.write_coil(21, True)
                        self.wait_for_state([1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 16, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]:
                        print("완료 : 로봇 서보 온 완료")
                        print("시도 : 로봇 스크립트 시작")
                        self.write_coil(21, False)
                        self.write_coil(22, True)
                        self.write_coil(23, True)
                        self.write_coil(24, False)
                        time.sleep(1)
                        self.write_coil(21, True)
                        self.wait_for_state([1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 16, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]:
                        print("시도 : 로봇 스크립트 정지")
                        self.write_coil(24, False)
                        self.write_coil(22, False)
                        self.write_coil(23, False)
                        self.write_coil(21, False)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 16, 1, 0, 0, 0, 0]:
                        print("완료 : 로봇 스크립트 시작 완료")
                        print("시도 : 스크립트 정지")
                        self.write_coil(24, False)
                        self.write_coil(22, False)
                        self.write_coil(23, False)
                        self.write_coil(21, False)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 5, 1, 0, 1, 0, 0]:
                        print("완료 : 가벼운 충돌 상태-이동 필요")
                        print("시도 : 로봇 스크립트 정지")
                        self.write_coil(24, False)
                        self.write_coil(22, False)
                        self.write_coil(23, False)
                        self.write_coil(21, False)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 5, 1, 0, 1, 0, 0]:
                        print("완료 : 가벼운 충돌 상태-이동 필요")
                        print("시도 : 로봇 스크립트 정지")
                        self.write_coil(24, False)
                        self.write_coil(22, False)
                        self.write_coil(23, False)
                        self.write_coil(21, False)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 5, 1, 0, 1, 0, 0]:
                        print("완료 : 노란색 불")
                        self.write_coil(20, False)
                        time.sleep(2)
                        self.write_coil(16, False)
                        self.write_coil(17, False)
                        self.write_coil(21, False)
                        time.sleep(2)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])

                    case [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 5, 1, 0, 1, 0, 0]:
                        print("완료 : 노란색 불")
                        self.write_coil(20, False)
                        time.sleep(2)
                        self.write_coil(16, False)
                        self.write_coil(17, False)
                        self.write_coil(21, False)
                        time.sleep(2)
                        self.wait_for_state([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0])


                    case _:
                        print("알 수 없는 상태입니다. 다음 반복을 실행합니다.")
                        time.sleep(2)

        except KeyboardInterrupt:
            print("프로그램이 중단되었습니다.")
        finally:
            self.client.close()
            print("Modbus 클라이언트 연결 종료")

# [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]
# [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 15, 1, 0, 0, 0, 0]
# 최초 부팅 중 : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0]
#              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

if __name__ == "__main__":
    master = ModbusMaster()
    master.main()
