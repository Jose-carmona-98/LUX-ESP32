import time
class BH1750:
    PWR_ON = 0x01       # encender
    CONT_HI_RES = 0x10  # continuo, alta resolucion
    def __init__(self, i2c, addr=0x23):
        self.i2c = i2c
        self.addr = addr
        self.pwr_on()
    def pwr_on(self):
        self.i2c.writeto(self.addr,
                         bytes([self.PWR_ON]))
    def luminance(self, mode=CONT_HI_RES):
        self.i2c.writeto(self.addr, bytes([mode]))
        time.sleep_ms(180)   # > 120 ms de integracion
        d = self.i2c.readfrom(self.addr, 2)
        n = (d[0] << 8) | d[1]   # 16 bits
        return n / 1.2           # lux, ec. (1)
