from machine import Pin, I2C
# import Adafruit_SSD1306 as disp

Pin('LED', Pin.OUT).value(1)
# I2C address of the SSD1306 display
dispAddr = 0x3C

i2c = I2C(scl=Pin(17, Pin.PULL_UP), sda=Pin(16,Pin.PULL_UP), freq=400000)

# Create the display object
# oled = disp.SSD1306_128_64(i2c, dispAddr)

# write hello world to the display
# oled.clear() 

# creat an I2C bus
i2c = I2C(scl=Pin('X1'), sda=Pin('X2'))

# scan for list of attached devices
dev_list = i2c.scan()
print(dev_list)
