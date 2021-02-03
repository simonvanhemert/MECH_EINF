""" Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
    author:         Raphael Andonie, Simon van Hemert
    date:           2020-04-06
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import pigpio
import time
import signal
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
drivetime = 2   # Time [s] for which to drive in each direction

# Turn on the motordriver -> 1
pi1.write(D2, 1)


""" Endless loop """
print("Start Event Log ...")
print("Press Ctrl+C to interrupt")
try:
    while True:
        pi1.write(A1, 1)        # Set channel A1
        pi1.write(A2, 0)        # Set channel A2
        time.sleep(drivetime)   # Drive for the set drivetime [s]

        pi1.write(A1, 0)        # Set channel A1
        pi1.write(A2, 1)        # Set channel A2
        time.sleep(drivetime)   # Drive for the set drivetime [s]

except KeyboardInterrupt:
    Motor_Off.turn_motor_off()          # Turn off DCmotor
    pass
