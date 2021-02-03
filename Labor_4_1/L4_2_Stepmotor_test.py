""" Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-06
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
    Motor_Off.turn_motor_off()          # Turn off Stepmotor
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
direction = 1       # Direction [-], 0 or 1
stoptime = 1        # Pause [s] between driving back and forth
step_number = 9600  # Number of steps [] to drive in each direction
cycle_number = 2    # Number of cycles to go through

# Initialisation
if direction == 1:
    Blevel = 1
    Blevel_ = 0
else:
    Blevel = 0
    Blevel_ = 1

step = 0
cycle = 0

""" Run Motor """
try:
    while cycle < cycle_number:         # For cycle_number cycles:
        while step < step_number:         # For step_number steps:
            # Turn on Motordriver -> 1
            pi1.write(D1, 1)
            pi1.write(D2, 1)

            pi1.write(A1, 0)        # Set A1 to 0/low
            pi1.write(A2, 1)        # Set A2 to 1/high
            time.sleep(steptime)    # Wait for steptime seconds

            pi1.write(B1, Blevel)   # Set B1 to 0 or 1, depending on direction
            pi1.write(B2, Blevel_)  # Set B2 to 0 or 1, depending on direction
            time.sleep(steptime)    # Wait for steptime seconds

            pi1.write(A1, 1)        # Set A1 to 1/high
            pi1.write(A2, 0)        # Set A2 to 0/low
            time.sleep(steptime)    # Wait for steptime seconds

            pi1.write(B1, Blevel_)  # Set B1 to 0 or 1, depending on direction
            pi1.write(B2, Blevel)   # Set B2 to 0 or 1, depending on direction
            time.sleep(steptime)    # Wait for steptime seconds

            step += 1               # Increment step counter
        cycle += 1                  # Increment cycle counter
        step = 0                    # Reset step counter
        Blevel = not Blevel         # Invert direction
        Blevel_ = not Blevel_       # Invert direction


except KeyboardInterrupt:
    Motor_Off.turn_motor_off()          # Turn off Stepmotor
    pass

