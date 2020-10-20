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

    os._exit(0)


signal.signal(signal.SIGINT, receiveSignal)

## Main Body
port_ledbar = 0  # TODO: Put Ledbar to grovepi digital connector D6

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

    print()		# TODO: print Ausgabe des eingegebenen Wertes zwischen 0 und 10

