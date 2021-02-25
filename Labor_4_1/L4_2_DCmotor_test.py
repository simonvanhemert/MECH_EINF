""" Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-22
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import pigpio
import signal
import time
from Motor_Off import Motor_Off


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of Motor,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    Motor_Off.turn_motor_off()          # Turn off DCmotor
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Initialize Grovepi
pi1 = pigpio.pi()    # Creates an Object from pi-class.

# Set ports
A1 = 20         # A  or M1
A2 = 21         # A/ or M2
D2 = 26         # N/ -> Turn on the motordriver A A/

# Settings
voltage = 6         # Voltage for DC motor [V] between 0 und 12 V (Voltage from power supply is always 12 V)
direction = 1       # Direction [-], 0 or 1
stoptime = 0.5        # Pause [s] between driving back and forth . standad = 1 [s]
drivetime = 1       # Time [s] for each step of stepmotor. standard = 2 [s]
cycle_number = 2    # Number of cycles to go through

# Initialisation
dutycycle = round(21.25 * voltage, 0)   # Calculate PWM dutycycle from 0 (OFF) to 255 bit (FULLY ON)
cycle = 0


""" Run Motor """
try:
    # Turn on the motordriver -> 1
    pi1.write(D2, 1)

    while cycle < cycle_number:         # For cycle_number cycles:
        if direction == 0:
            # Set PWM on A1
            pi1.set_PWM_frequency(A1, 4000)         # Frequency of the PWM Signals [Hz] -> 4000
            pi1.set_PWM_dutycycle(A1, dutycycle)    # Set the calculated dutycycle
            # Set 0 on A2
            pi1.write(A2, 0)
        elif direction == 1:
            # Set 0 on A1
            pi1.write(A1, 0)                        # Set the other chanel to 0
            # Set PWM on A2
            pi1.set_PWM_frequency(A2, 4000)         # Frequency of the PWM Signals [Hz] -> 4000
            pi1.set_PWM_dutycycle(A2, dutycycle)    # Set the calculated dutycycle
        time.sleep(drivetime)                       # Drive for drivetime [s]

        # Turn of motor to wait:
        pi1.write(A1, 0)
        pi1.write(A2, 0)

        cycle += 0.5                # Increment cycle counter
        direction = not direction   # Invert direction
        time.sleep(stoptime)        # Wait for stoptime [s]

except KeyboardInterrupt:
    pass

Motor_Off.turn_motor_off()  # Turn off DCmotor
