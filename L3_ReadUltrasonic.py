# Labor 3, Parksensor, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

## Import Packages
import signal, os, grovepi


## Definitions
# Exit procedure in case of CTRL+C
def receiveSignal(signalNumber, frame):
    print "Received: ", signalNumber
    print "Exit Python!"
    os._exit(0)


signal.signal(signal.SIGINT, receiveSignal)


## Main Body
ultrasonic_ranger = 4  # Connect the Grove Ultrasonic Ranger to digital port D4

# Continuously run the following:
while True:
    # Read and print distance value from Ultrasonic
    print grovepi.ultrasonicRead(ultrasonic_ranger), 'cm'

