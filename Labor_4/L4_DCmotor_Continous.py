""" Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-06
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import pigpio
import signal
from Motor_Off import turn_motor_off


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of Motor,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    turn_motor_off()          # Turn off DCmotor
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Initialize Grovepi
pi1 = pigpio.pi()   # Creates an Object from pi-class.

# Set ports
A1 = 20         # A  or M1
A2 = 21         # A/ or M2
D2 = 26         # N/ -> Turn on the motordriver A A/


""" Run Motor """
try:
    # Turn on Motordriver -> 1
    pi1.write(D2, 1)

    # Turn on Motor
    pi1.write(A1, 1)        # Set channel A1
    pi1.write(A2, 0)        # Set channel A2

    # Ask for any user input to Quit
    userinput = input("Stop motor? (Press Enter for yes)")
except KeyboardInterrupt:
    pass

# Turn off DCmotor
turn_motor_off()
