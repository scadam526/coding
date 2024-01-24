import machine

# Define the PWM pin
pwm_pin = machine.Pin(0)

# Initialize PWM object
pwm = machine.PWM(pwm_pin)


def set_pwm(duty_cycle, frequency):
    """
    Set the duty cycle and frequency of the PWM output.

    :param duty_cycle: Duty cycle value (0 to 1023)
    :param frequency: PWM frequency in Hz
    """
    
    # duty_cycle = (duty_cycle / 100) * 1023
    pwm.duty_u16(int(duty_cycle * 65535 / 1023))  # Convert 10-bit duty cycle to 16-bit
    pwm.freq(int(frequency*1000))
    

# Example usage
# set_pwm(0, 200)  # Set duty cycle to 50% and frequency to 1000 Hz
