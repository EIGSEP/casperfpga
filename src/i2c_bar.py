import time, numpy as np, logging
from .i2c import I2C_DEVICE


class MS5611_01B(I2C_DEVICE):

    OSR_PRESS = {   256:0x40,
            512:0x42,
            1024:0x44,
            2048:0x46,
            4096:0x48,}

    OSR_TEMP = {    256:0x50,
            512:0x52,
            1024:0x54,
            2048:0x56,
            4096:0x58,}

    D1_MIN, D1_MAX = 0, 16777216
    D2_MIN, D2_MAX = 0, 16777216
    DT_MIN, DT_MAX = -16776960, 16777216
    TEMP_MIN, TEMP_MAX = -4000, 8500
    OFF_MIN, OFF_MAX = -8589672450, 12884705280
    SENS_MIN, SENS_MAX = -4294836225, 6442352640
    P_MIN, P_MAX = 1000, 120000

    def __init__(self, itf, addr=0x77, **kwargs):
        super(MS5611_01B, self).__init__(itf, addr, **kwargs)
        self._tsampling = 0.01
        self.prom = self.readCalibration()

    def init(self):
        self.reset()
        self.prom = self.readCalibration()

    def readCalibration(self):
        data = []
        for i in range(8):
            data += self.read(0xa0|(i<<1),2)
        data = [x<<8|y for x,y in zip(data[0::2],data[1::2])]

        if data[7] & 0xf != self.crc4(data):
            raise IOError('Barometer MS5611-01B PROM CRC error!')

        return data

    def crc4(self,data):
        """ input: 16bit * 8 data list
        """

        n_rem = 0
        crc_read = data[7] & 0xff
        data[7] = 0xff00 & data[7]

        for i in range(16):
            if i%2:
                n_rem ^= (data[i>>1] & 0xff)
            else:
                n_rem ^= (data[i>>1] >> 8)
            for n_bit in range(8,0,-1):
                if n_rem & 0x8000:
                    n_rem = (n_rem << 1) ^ 0x3000
                else:
                    n_rem = (n_rem << 1)
        n_rem = (0x000f & (n_rem >> 12))

        data[7] = crc_read | data[7]

        return (n_rem ^ 0x0)

    def readPress(self,rawtemp=None,dt=None,osr=4096):
        """ 
        Return air pressure

        .. code-block:: python

            readPress()     # return raw data with osr=4096
            readPress(2007,2366)    # return return compensated data with osr=4096

        To get rawtemp and dt:
        
        .. code-block:: python

            rawtemp, dt = readTemp(raw=True)
        """
        if osr not in self.OSR_PRESS:
            raise ValueError("Invalid parameter")
        self.write(self.OSR_PRESS[osr])
        time.sleep(self._tsampling)
        data = self.read(0x00,3)
        data = (data[0]<<16)|(data[1]<<8)|data[2]

        if rawtemp == None or dt == None:
            return data
        else:
            off = self.prom[2] * 65536 + self.prom[4] * dt / 128 
            sens = self.prom[1] * 32768 + self.prom[3] * dt / 256

            t2=0
            off2=0
            sens2=0
            if rawtemp < 2000:
                t2 = (dt**2.)/(1<<31)
                off2 = 5 * ((rawtemp-2000.)**2) / 2
                sens2 = 5 * ((rawtemp-2000.)**2) / 4
            if rawtemp < -1500:
                off2 = off2 + 7 * ((rawtemp+1500.)**2)
                sens2 = sens2 + 11 * ((rawtemp+1500.)**2) / 2

            rawtemp=rawtemp-t2
            off=off-off2
            sens=sens-sens2

        if data < self.D1_MIN or data > self.D1_MAX or \
            off < self.OFF_MIN or off > self.OFF_MAX or \
            sens < self.SENS_MIN or sens > self.SENS_MAX:
            raise IOError('Compensation values excceed min-max range.')

        data = (data * 1. / (1<<21) * sens - off) / (1<<15)
        if data < self.P_MIN or data > self.P_MAX:
            raise IOError('Temperature compensated pressure excceeds min-max range')

        return data/100.

    def readTemp(self,raw=False,osr=4096):
        """ 
        Return the temperature

        .. code-block:: python

            readTemp()      # return the temperature
            readTemp(raw=True)  # return the raw temperature data together with dt
        """
        if osr not in self.OSR_TEMP:
            raise ValueError("Invalid parameter")
        self.write(self.OSR_TEMP[osr])
        time.sleep(0.1)
        data = self.read(0x00,3)
        data = (data[0]<<16)|(data[1]<<8)|data[2]

        dt = data - self.prom[5] * (1<<8) * 1.0

        data = 2000 + dt * self.prom[6] / (1<<23)

        if data < self.TEMP_MIN or data > self.TEMP_MAX or \
            dt < self.DT_MIN or dt > self.DT_MAX:
            raise IOError('Temperature excceeds min-max range')

        if raw==False:
            return data / 100.
        else:
            return data,dt

    def toAltitude(self,bar,temp,P0=1013.25):
        """ 
        Convert air pressure and temperature to altitude
        
        * bar is air pressure, temp is temperature
        * P0 is air presure at sea level

        .. code-block:: python

            toAltitude(1000.09,20.07)

        To get raw temp:

        .. code-block:: python

           rawtemp, dt = readTemp(raw=True)
        
        To get bar:
        
        .. code-block:: python

           bar = readPress(rawtemp, dt)
        """
        return ((P0/bar)**(1/5.257)-1)*(temp+273.15)/0.0065

    def reset(self):
        self.write(0x1e)
        time.sleep(0.1)

    def read(self,reg=None,length=1):
        return self.itf.read(self.addr,reg,length)

    def write(self,reg=None,data=None):
        self.itf.write(self.addr,reg,data)
