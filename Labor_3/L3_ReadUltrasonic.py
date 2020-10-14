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
port_ranger = 000  # TODO: Put Ultra Sonic Ranger to grovepi digital connector D5

# Continuously run the following:
while True:
    # Read and print distance value from Ultrasonic
    print(grovepi.ultrasonicRead(port_ranger), 'cm')

