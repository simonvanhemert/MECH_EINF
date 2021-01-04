""" Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-06
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import pigpio
import time
from Motor_Off import turn_motor_off


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of Motor,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    turn_motor_off()          # Turn off stepmotor
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Initialize Grovepi
pi1 = pigpio.pi()   # Creates an Object from pi-class.

# Set ports
A1 = 20     # A  or M1
A2 = 21     # A/ or M2
B1 = 6      # B  or M3
B2 = 13     # B/ or M4
D1 = 12     # N  -> Turn on the motordriver B B/
D2 = 26     # N/ -> Turn on the motordriver A A/

# Settings
steptime = 0.001    # Time [s] for each step of stepmotor. In fact sets motor speed.


""" Run Motor """
try:
    while True:         # For ever:
        # Turn on Motordriver -> 1
        pi1.write(D1, 1)
        pi1.write(D2, 1)

        pi1.write(B1, 1)        # Set B1 to 1/high
        pi1.write(B2, 0)        # Set B2 to 0/low
        time.sleep(steptime)    # Wait for steptime seconds

        pi1.write(A1, 0)        # Set A1 to 0/low
        pi1.write(A2, 1)        # Set A2 to 1/high
        time.sleep(steptime)    # Wait for steptime seconds

        pi1.write(B1, 0)        # Set B1 to 0/low
        pi1.write(B2, 1)        # Set B2 to 1/high
        time.sleep(steptime)    # Wait for steptime seconds

        pi1.write(A1, 1)        # Set A1 to 1/high
        pi1.write(A2, 0)        # Set A2 to 0/low
        time.sleep(steptime)    # Wait for steptime seconds

except KeyboardInterrupt:
    # Turn off stepmotor
    turn_motor_off()
    pass

