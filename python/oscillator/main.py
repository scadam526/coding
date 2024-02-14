from time import sleep
from machine import Pin, PWM, ADC

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

duty = 87
freq = 100
pwm = PWM(Pin(2))

def set_pwm(freq_kHz, duty):
    freq = freq_kHz * 1000
    pwm.freq(freq)
    duty_u16 = int((duty/100)*2**16)
    pwm.duty_u16(duty_u16)

def sweep_pwm():
    for i in range(100):
        set_pwm(freq, i)
        if vpeak.read_u16() > pk:
            pk = vpeak.read_u16()
        print(vpeak.read_u16())
        sleep(0.1)

def irqHandler(p):
    print(f"Button pressed: {p}")
    buttons()

def buttons():
    global duty, freq
    pk = 0
    while sw1.value() == 0:
        duty -= 0.1
        if duty > 100:
            duty = 100
        set_pwm(freq, duty)
        sleep(0.1)
    while sw2.value() == 0:
        duty += 0.1
        if duty < 0:
            duty = 0
        set_pwm(freq, duty)
        sleep(0.1)
    if sw3.value() == 0:
        sweep_pwm()

sw1.irq(trigger=Pin.IRQ_FALLING, handler=irqHandler)
sw2.irq(trigger=Pin.IRQ_FALLING, handler=irqHandler)
sw3.irq(trigger=Pin.IRQ_FALLING, handler=irqHandler)

set_pwm(freq, duty)
while True:
    print(vpeak.read_u16())
    sleep(0.5)