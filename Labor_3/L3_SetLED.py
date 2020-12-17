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
port_ledbar = 2     # Put Ledbar to grovepi digital connector D2

# Initialize LED Bar
grovepi.ledBar_init(port_ledbar, 0)
grovepi.ledBar_orientation(port_ledbar, 1)
grovepi.pinMode(port_ledbar, "OUTPUT")

# Settings
ledbar_nof_levels = 10      # Number of LEDs


""" Endless loop """
print("Start Event Log ...")
while True:
    # Ask for a user input between 0 and 10
    userinput = input('Geben sie einen Wert zwischen 0 und 10 ein: ')
    # Save as integer
    userinput = int(userinput)

    # Set ledbar level
    if userinput >= 0 or userinput <= ledbar_nof_levels:
        grovepi.ledBar_setLevel(port_ledbar, userinput)

    print(userinput)		# Print the given value to screen


