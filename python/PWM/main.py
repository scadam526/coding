import machine

# Define the PWM pin
pwm_pin = machine.Pin(0)

# Initialize PWM object
pwm = machine.PWM(pwm_pin)

def set_pwm(freq_kHz, duty):
    freq = freq_kHz * 1000
    pwm.freq(freq)
    duty_u16 = int((duty/100)*2**16)
    pwm.duty_u16(duty_u16)
