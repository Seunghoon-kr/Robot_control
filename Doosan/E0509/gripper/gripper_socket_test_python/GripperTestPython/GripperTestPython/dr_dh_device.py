tp_popup(“socket open success”, DR_PM_ALARM)

class dr_dh_device(object):

    def dr_connect_device(self):
        ret = -1
        baudrate = 115200
        bytesize = 8
        parity = "N"
        stopbits = 1
        serial_isopen = flange_serial_open(baudrate, bytesize, parity, stopbits)

        if serial_isopen == 0:
            #tp_popup(“socket open success”, DR_PM_ALARM)
            ret = 0
        elif serial_isopen < 0:
            #tp_popup(“socket open error”, DR_PM_ALARM)
            ret = -1
        return ret

    def dr_disconnect_device(self):
        flange_serial_close()

    def dr_device_write(self, write_data):
        ret = flange_serial_write(write_data)
        if ret == 0:
            # tp_log(“socket send success”)
            return 0
        else:
            return -1

    def dr_device_read(self, wlen):
        responseData = [0, 0, 0, 0, 0, 0, 0, 0]
        res, responseData = flange_serial_read(timeout = 5)
        if res not in [1,2]:
            return responseData
        else:
            return -1

    """description of class"""


#===================================================================

m_device = dr_dh_device()

class dr_dh_modbus_gripper(object):
    gripper_ID = 0x01

    def CRC16(self, nData, wLength):
        if nData == 0x00:
            return 0x0000
        wCRCWord = 0xFFFF
        poly = 0xA001
        for num in range(wLength):
            date = nData[num]
            wCRCWord = (date & 0xFF) ^ wCRCWord
            for bit in range(8):
                if (wCRCWord & 0x01) != 0:
                    wCRCWord >>= 1
                    wCRCWord ^= poly
                else:
                    wCRCWord >>= 1
        return wCRCWord

    def gripper_serial_open(self):
        ret = 0
        ret = m_device.dr_connect_device()
        if (ret < 0):
            print('open failed')
            return ret
        else:
            print('open successful')
            return ret

    def gripper_serial_close(self):
        m_device.dr_disconnect_device()

    def WriteRegisterFunc(self, index, value):
        send_buf = [0, 0, 0, 0, 0, 0, 0, 0]
        send_buf[0] = self.gripper_ID
        send_buf[1] = 0x06
        send_buf[2] = (index >> 8) & 0xFF
        send_buf[3] = index & 0xFF
        send_buf[4] = (value >> 8) & 0xFF
        send_buf[5] = value & 0xFF

        crc = self.CRC16(send_buf, len(send_buf) - 2)
        send_buf[6] = crc & 0xFF
        send_buf[7] = (crc >> 8) & 0xFF

        send_temp = send_buf
        data = ""
        for i in send_temp:
            data += str(i)
            data += " "

        ret = False
        retrycount = 3

        while (ret == False):
            ret = False

            if (retrycount < 0):
                break
            retrycount = retrycount - 1

            wdlen = m_device.dr_device_write(data)
            if (len(send_temp) != wdlen):
                print('write error ! write : ', send_temp)
                continue

            rev_buf = m_device.dr_device_read(8)
            if (len(rev_buf) == wdlen):
                ret = True
        return ret

    def ReadRegisterFunc(self, index):
        send_buf = [0, 0, 0, 0, 0, 0, 0, 0]
        send_buf[0] = self.gripper_ID
        send_buf[1] = 0x03
        send_buf[2] = (index >> 8) & 0xFF
        send_buf[3] = index & 0xFF
        send_buf[4] = 0x00
        send_buf[5] = 0x01

        crc = self.CRC16(send_buf, len(send_buf) - 2)
        send_buf[6] = crc & 0xFF
        send_buf[7] = (crc >> 8) & 0xFF

        send_temp = send_buf
        ret = False
        retrycount = 3

        while (ret == False):
            ret = False

            if (retrycount < 0):
                break
            retrycount = retrycount - 1

            wdlen = m_device.dr_device_write(send_temp)
            if (len(send_temp) != wdlen):
                print('write error ! write : ', send_temp)
                continue

            rev_buf = m_device.dr_device_read(7)
            if (len(rev_buf) == 7):
                value = ((rev_buf[4] & 0xFF) | (rev_buf[3] << 8))
                ret = True
            # ('read value : ', value)
        return value

    def Initialization(self):
        self.WriteRegisterFunc(0x0100, 0xA5)

    def SetTargetPosition(self, refpos):
        self.WriteRegisterFunc(0x0103, refpos);

    def SetTargetForce(self, force):
        self.WriteRegisterFunc(0x0101, force);

    def SetTargetSpeed(self, speed):
        self.WriteRegisterFunc(0x0104, speed);

    def GetCurrentPosition(self):
        return self.ReadRegisterFunc(0x0202);

    def GetCurrentTargetForce(self):
        return self.ReadRegisterFunc(0x0101);

    def GetCurrentTargetSpeed(self):
        return self.ReadRegisterFunc(0x0104);

    def GetInitState(self):
        return self.ReadRegisterFunc(0x0200);

    def GetGripState(self):
        return self.ReadRegisterFunc(0x0201);

    """description of class"""


#===================================================================

m_gripper = dr_dh_modbus_gripper()

def modbus_gripper():
    port = 'com7'
    baudrate = 115200
    initstate = 0
    g_state = 0
    force = 100
    speed = 100

    m_gripper.gripper_serial_open()
    m_gripper.Initialization()
    print('Send grip init')

    while (initstate != 1):
        initstate = m_gripper.GetInitState()
        wait(0.2)

    m_gripper.SetTargetForce(force)
    m_gripper.SetTargetSpeed(speed)

    while True:
        g_state = 0
        m_gripper.SetTargetPosition(0)
        while (g_state == 0):
            g_state = m_gripper.GetGripState()
            wait(0.2)

        g_state = 0;
        m_gripper.SetTargetPosition(1000)
        while (g_state == 0):
            g_state = m_gripper.GetGripState()
            wait(0.2)
    m_gripper.gripper_serial_close()

if __name__ == '__main__':
    # socket_gripper()
    modbus_gripper()



