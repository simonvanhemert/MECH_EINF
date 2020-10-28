# Labor 3, Parksensor, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

## Import Packages
import signal
import os
import grovepi


## Definitions
# Exit procedure in case of CTRL+C
def receiveSignal(signalNumber, frame):
    print("Received: ", signalNumber)
    print("Exit Python!")

    # Turn of LED bar
    # TODO: Set LED bar level to 0 in case of Exit Procedure
    # TODO: Search for the method to set the LED bar level in this programm, and use that method here to set to 0

    os._exit(0)


signal.signal(signal.SIGINT, receiveSignal)

## Main Body
# TODO set the Port to the correct value. The letter D oder A is ommited.
port_ledbar = 0     # Put Ledbar to grovepi digital connector D2

# Initialize LED Bar
grovepi.ledBar_init(port_ledbar, 0)
grovepi.ledBar_orientation(port_ledbar, 1)
grovepi.pinMode(port_ledbar, "OUTPUT")

# Continuously run the following:
while True:
    eingabe = input('Geben sie einen Wert zwischen 0 und 10 ein: ')
    wert = int(eingabe)

    if wert >= 0 or wert <= 10:
        grovepi.ledBar_setLevel(port_ledbar, wert)

    print()		# TODO: Print the given value to screen
                # TODO: Use the print() method and the value for the distance resulting from the input.


