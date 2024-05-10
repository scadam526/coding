from machine import Pin, I2C
from ssd1306 import SSD1306_I2C as oled
import time

# turn on pico LED
led = Pin('LED', Pin.OUT)
led.value(0)

# I2C bus 0
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
addr = 0x3d
disp = oled(128, 64, i2c, addr)

disp.init_display()
while True:
    disp.fill(0)
    # time = milliseconds
    disp.text(str(time.ticks_ms()), 0, 0)
    disp.show()