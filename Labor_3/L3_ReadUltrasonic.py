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
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Set sensor ports and settings
port_ranger = 5  # Put Ultra Sonic Ranger to grovepi digital connector D5


""" Endless loop """
print("Start Event Log ...")
while True:
    dist = grovepi.ultrasonicRead(port_ranger)  # Measure distance

    # Print distance value from the Ultrasonic sensor.
    print(dist, 'cm')

