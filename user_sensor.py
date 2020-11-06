from bluepy.btle import UUID, Peripheral, DefaultDelegate, AssignedNumbers
import struct
import math
import time

def _TI_UUID(val):
    return UUID("%08X-0451-4000-b000-000000000000" % (0xF0000000+val))

# Sensortag versions
AUTODETECT = "-"
SENSORTAG_V1 = "v1"
SENSORTAG_2650 = "CC2650"

class SensorBase:
    # Derived classes should set: svcUUID, ctrlUUID, dataUUID
    sensorOn  = struct.pack("B", 0x01)
    sensorOff = struct.pack("B", 0x00)

    def __init__(self, periph):
        self.periph = periph
        self.service = None
        self.ctrl = None
        self.data = None

    def enable(self):
        if self.service is None:
            self.service = self.periph.getServiceByUUID(self.svcUUID)
        if self.ctrl is None:
            self.ctrl = self.service.getCharacteristics(self.ctrlUUID) [0]
        if self.data is None:
            self.data = self.service.getCharacteristics(self.dataUUID) [0]
        if self.sensorOn is not None:
            self.ctrl.write(self.sensorOn,withResponse=True)

    def read(self):
        return self.data.read()

    def disable(self):
        if self.ctrl is not None:
            self.ctrl.write(self.sensorOff)
	

class MovementSensorMPU9250(SensorBase):
    svcUUID  = _TI_UUID(0xAA80)
    dataUUID = _TI_UUID(0xAA81)
    ctrlUUID = _TI_UUID(0xAA82)
    periodUUID = _TI_UUID(0xAA83)

    sensorOn = None
    GYRO_XYZ =  7
    ACCEL_XYZ = 7 << 3
    MAG_XYZ = 1 << 6
    ACCEL_RANGE_2G  = 0 << 8
    ACCEL_RANGE_4G  = 1 << 8
    ACCEL_RANGE_8G  = 2 << 8
    ACCEL_RANGE_16G = 3 << 8

    def __init__(self, periph):
        SensorBase.__init__(self, periph)
        self.ctrlBits = 0

    def enable(self, bits):
        SensorBase.enable(self)
        self.ctrlBits |= bits
        self.ctrl.write( struct.pack("<H", self.ctrlBits) )

    def disable(self, bits):
        self.ctrlBits &= ~bits
        self.ctrl.write( struct.pack("<H", self.ctrlBits) )

    def rawRead(self):
        dval = self.data.read()
        return struct.unpack("<hhhhhhhhh", dval)

class AccelerometerSensorMPU9250:
    def __init__(self, sensor_):
        self.sensor = sensor_
        self.bits = self.sensor.ACCEL_XYZ | self.sensor.ACCEL_RANGE_4G
        self.accScale = 4.0/32768.0
        self.gyroScale = 500.0/65536.0

    def enable(self):
        self.sensor.enable(self.bits)
        self.sensor.enable(self.sensor.GYRO_XYZ)

    def disable(self):
        self.sensor.disable(self.bits)
        self.sensor.disable(self.sensor.GYRO_XYZ)

    def read(self):
        '''Returns (x_accel, y_accel, z_accel) in units of g'''
        rawVals = self.sensor.rawRead()[0:6]
        accelTuple = tuple([ round(v*self.accScale,2) for v in rawVals[3:6]])
        gyroTuple = tuple([ round(v*self.gyroScale,2) for v in rawVals[0:3]])
        return (accelTuple + gyroTuple)

class HumiditySensorHDC1000(SensorBase):
    svcUUID  = _TI_UUID(0xAA20)
    dataUUID = _TI_UUID(0xAA21)
    ctrlUUID = _TI_UUID(0xAA22)

    def __init__(self, periph):
        SensorBase.__init__(self, periph)

    def read(self):
        '''Returns (ambient_temp, rel_humidity)'''
        (rawT, rawH) = struct.unpack('<HH', self.data.read())
        temp = -40.0 + 165.0 * (rawT / 65536.0)
        RH = 100.0 * (rawH/65536.0)
        return (temp, RH)

class KeypressSensor(SensorBase):
    svcUUID = UUID(0xFFE0)
    dataUUID = UUID(0xFFE1)
    ctrlUUID = None
    sensorOn = None

    def __init__(self, periph):
        SensorBase.__init__(self, periph)
 
    def enable(self):
        SensorBase.enable(self)
        self.char_descr = self.service.getDescriptors(forUUID=0x2902)[0]
        self.char_descr.write(struct.pack('<bb', 0x01, 0x00), True)

    def disable(self):
        self.char_descr.write(struct.pack('<bb', 0x00, 0x00), True)

class KeypressDelegate(DefaultDelegate):
    BUTTON_L = 0x02
    BUTTON_R = 0x01
    ALL_BUTTONS = (BUTTON_L | BUTTON_R)

    _button_desc = { 
        BUTTON_L : "Left button",
        BUTTON_R : "Right button",
        ALL_BUTTONS : "Both buttons"
    } 

    def __init__(self):
        DefaultDelegate.__init__(self)
        self.lastVal = 0

    def handleNotification(self, hnd, data):
        # NB: only one source of notifications at present
        # so we can ignore 'hnd'.
        val = struct.unpack("B", data)[0]
        down = (val & ~self.lastVal) & self.ALL_BUTTONS
        if down != 0:
            self.onButtonDown(down)
        up = (~val & self.lastVal) & self.ALL_BUTTONS
        if up != 0:
            self.onButtonUp(up)
        self.lastVal = val

    def onButtonUp(self, but):
        print ( "** " + self._button_desc[but] + " UP")

    def onButtonDown(self, but):
        print ( "** " + self._button_desc[but] + " DOWN")

class SensorTag(Peripheral):
    def __init__(self,addr,version=AUTODETECT):
        Peripheral.__init__(self,addr)
        self._mpu9250 = MovementSensorMPU9250(self)
        self.accelerometer = AccelerometerSensorMPU9250(self._mpu9250)
        self.humidity = HumiditySensorHDC1000(self)
        self.keypress = KeypressSensor(self)
     
def main():

    #Justin
    #my_sensor = 'f0:f8:f2:86:7b:83'
    #others
    #my_sensor = '54:6c:0e:53:3c:ae'
	# my_sensor = '54:6c:0e:53:35:cd'
    ##jeff sn
    # my_sensor = 'f0:f8:f2:86:bb:83'
    No_of_samples = 2
    tag = SensorTag(my_sensor)
    print("Connected to SensorTag", my_sensor)
    tag.accelerometer.enable()
    accelData_list = []
    time.sleep(1)
    print("Start!!")
    time.sleep(1)

    start = time.time()
    for i in range(No_of_samples*50):
        accelData = tag.accelerometer.read()
        # print(accelData)
        print(i)
        accelData_list.append(accelData)
    end = time.time()
    print("Recording Complete!")
    print("Time taken: %ds", end - start)
    tag.accelerometer.disable()
    tag.disconnect()

    return accelData_list

if __name__ == "__main__":
    main()
