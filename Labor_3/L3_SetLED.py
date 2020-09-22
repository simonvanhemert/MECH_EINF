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
    os._exit(0)


signal.signal(signal.SIGINT, receiveSignal)

## Main Body
ledbar = 5  # Connect the Grove LED Bar to digital port D5

# Initialize LED Bar
grovepi.ledBar_init(ledbar, 0)
grovepi.ledBar_orientation(ledbar, 1)
grovepi.pinMode(ledbar, "OUTPUT")

# Continuously run the following:
while True:
    eingabe = input('Geben sie einen Wert zwischen 0 und 10 ein: ')
    wert = int(eingabe)

    if wert >= 0 or wert <= 10:
        grovepi.ledBar_setLevel(ledbar, wert)

    print		# Ausgabe des eingegebenen Wertes zwischen 0 und 10

