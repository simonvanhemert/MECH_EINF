""" Labor 3, Parksensor, MECH_EINF Module WI HSLU T&A
    author:         Raphael Andonie, Simon van Hemert
    date:           2020-04-06
    organization:   HSLU T&A """

## Import Packages
import signal
import os
import grovepi


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of ledBar,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    # Turn of LED bar
    grovepi.ledBar_setLevel(port_ledbar, 0)
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Set sensor ports and settings
port_ledbar = 2  # Put Ledbar to grovepi digital connector D2
port_ranger = 5  # Put Ultra Sonic Ranger to grovepi digital connector D5

# Initialize LED Bar
grovepi.ledBar_init(port_ledbar, 0)
grovepi.ledBar_orientation(port_ledbar, 1)
grovepi.pinMode(port_ledbar, "OUTPUT")

# Settings
range_max = 30              # Max range
ledbar_nof_levels = 10      # Number of LEDs
lvl = 0                     # Starting level


""" Endless loop """
print("Start Event Log ...")
while True:
    dist = grovepi.ultrasonicRead(port_ranger)  # Measure distance

    # Find the appropriate number of LEDs, set to 0 if out of range.
    if dist <= range_max:
        lvl = int(- (ledbar_nof_levels / range_max) * dist + ledbar_nof_levels)
    else:
        lvl = 0

    # Set the LEDs
    if 0 <= lvl <= ledbar_nof_levels:
        grovepi.ledBar_setLevel(port_ledbar, lvl)

    # Print the LED level and current measured distance
    print(lvl, "<->", dist)

