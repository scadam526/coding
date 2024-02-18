from machine import Pin, I2C
from ssd1306 import SSD1306_I2C as oled
import random

# turn on pico LED
led = Pin('LED', Pin.OUT)
led.value(0)

# I2C bus 0
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
addr = 0x3d
disp = oled(128, 64, i2c, addr)
# Functions
def reg_write(i2c, addr, reg, data):
    # Construct message
    msg = bytearray()
    msg.append(data)
    
    # Write out message to register
    i2c.writeto_mem(addr, reg, msg)
    
def reg_read(i2c, addr, reg, nbytes=1):
    
    # Check to make sure caller is asking for 1 or more bytes
    if nbytes < 1:
        return bytearray()
    
    # Request data from specified register(s) over I2C
    data = i2c.readfrom_mem(addr, reg, nbytes)
    
    return data

disp.init_display()
while True:
    disp.fill(0)
    disp.pixel(random.randint(0,128), random.randint(0,64), 1)
    disp.pixel(random.randint(0,128), random.randint(0,64), 1)
    disp.pixel(random.randint(0,128), random.randint(0,64), 1)
    disp.pixel(random.randint(0,128), random.randint(0,64), 1)
    disp.show()
