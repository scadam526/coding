from time import sleep
from machine import Pin, PWM, ADC, I2C
from ssd1306 import SSD1306_I2C as oled
import _thread

led = Pin('LED', Pin.OUT)
led1 = Pin(10, Pin.OUT)
led2 = Pin(11, Pin.OUT)
led3 = Pin(12, Pin.OUT)
sw1 = Pin(6, Pin.IN, Pin.PULL_UP)
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw3 = Pin(8, Pin.IN, Pin.PULL_UP)
pgood = Pin(5, Pin.IN, Pin.PULL_UP)
vset = ADC(Pin(27))
vpeak = ADC(Pin(26))
vpeakDiv = 0.06
vref = 3.3
adcBits = 16
counts = 2**adcBits

duty = 95
freqTxNom = 110
freqPWM = 100 * 1000 # 100kHz
pwm = PWM(Pin(2))
nominalDuty = 95


i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oledAddr = 0x3d
oledWidth = 128
oledHeight = 64
print(len(i2c.scan()))

if len(i2c.scan()) > 0:
    disp = oled(oledWidth, oledHeight, i2c, oledAddr)
    disp.init_display()


def set_pwm(fTx):
    global freqPWM
    duty = 148.523 - 0.492 * fTx
    pwm.freq(freqPWM)
    duty_u16 = int((duty/100)*2**16)
    pwm.duty_u16(duty_u16)
    print(f"Duty: {duty}")


def irqHandler(p):
    print(f"Button pressed: {p}")
    buttons()


def buttons():
    global freqTx
    pk = 0
    while sw1.value() == 0:
        freqTx -= 0.1
        if freqTx > 100:
            freqTx = 100
        set_pwm(freqTx)
        sleep(0.1)
    while sw2.value() == 0:
        freqTx += 0.1
        if freqTx < 0:
            freqTx = 0
        set_pwm(freqTx)
        sleep(0.1)
    if sw3.value() == 0:
        freqTx = freqTxNom
        set_pwm(freqTx)


# start a background thread to write vset and vpeak to the OLED
def oledThread():
    while True:
        disp.fill(0)
        vsetVal = (vset.read_u16() / counts) * vref
        vpeakVal = ((vpeak.read_u16() / counts) * vref / vpeakDiv) + 0.82
        # display vsetVal to two decimal places
        # vsetVal = "{:.2f}".format(vsetVal)
        disp.text(f"Vset:  {vsetVal:.2f}V", 0, 0)
        disp.text(f"Vpeak: {vpeakVal:.2f}V", 0, 10)
        disp.text(f"Freq:  {freqTx:.1f}kHz", 0, 20)
        disp.show()
        sleep(0.1)


sw1.irq(trigger=Pin.IRQ_FALLING, handler=irqHandler)
sw2.irq(trigger=Pin.IRQ_FALLING, handler=irqHandler)
sw3.irq(trigger=Pin.IRQ_FALLING, handler=irqHandler)

freqTx = freqTxNom
set_pwm(freqTx)

if len(i2c.scan()) > 0:
    _thread.start_new_thread(oledThread, ())
else: print("OLED not found")