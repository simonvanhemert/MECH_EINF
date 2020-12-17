""" Labor 1, Hysterese, MECH_EINF Module WI HSLU T&A
    author:         Raphael Andonie, Simon van Hemert
    date:           2020-04-22
    organization:   HSLU T&A  """

## Import Packages
import os
import grovepi
import signal


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received,
    - print signal number,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Set sensor ports and settings
port_sensor = 2     # Connect Sensor to Digital port D2
sensorsignal = False

grovepi.pinMode(port_sensor, "INPUT")


""" Endless loop """
print("Start Event Log ...")
while True:
    # When the last signal is not equal to the current signal
    if sensorsignal != grovepi.digitalRead(port_sensor):
        # Set the signal to the current signal
        sensorsignal = grovepi.digitalRead(port_sensor)
        # Print the change of signal
        print("Signal : ", "[", sensorsignal, "]")
