""" Labor 1, Hysterese, MECH_EINF Module WI HSLU T&A
    author:         Raphael Andonie, Simon van Hemert
    date:           2020-04-22
    organization:   HSLU T&A  """

## Import Packages
import os
import signal
import grovepi


# Definition for recieved exit or error signal:
def receiveSignal(signalNumber, frame):
    print("Received: ", signalNumber)
    print("Exit Python!")
    os._exit(0)

signal.signal(signal.SIGINT, receiveSignal)

# Connect the Proximity Sensor to analog port D2
port_sensor = 2     # Connect Sensor
signal = False

grovepi.pinMode(port_sensor, "INPUT")

print("Start Event Log ...")

while True:
    if signal != grovepi.digitalRead(port_sensor):
        signal = not signal
        print("Signal : ", "[", signal, "]")
