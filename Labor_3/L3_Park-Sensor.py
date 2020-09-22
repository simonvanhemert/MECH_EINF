# Labor 3, Parksensor, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

## Import Packages
import signal, os, grovepi


## Definitions
def receiveSignal(signalNumber, frame):
    print("Received: ", signalNumber)
    print("Exit Python!")

    # TODO: Turnoff all lights when exit
    # grovepi.ledBar_setLevel(port_ledbar, 0)

    os._exit(0)


signal.signal(signal.SIGINT, receiveSignal)


## Main Body
port_ledbar = 000  # FIXME: Put Ledbar to grovepi digital connector 1
port_ranger = 000  # FIXME: Put Ultra Sonic Ranger to grovepi digital connector 2

# Initialize LED Bar
grovepi.ledBar_init(port_ledbar, 0)
grovepi.ledBar_orientation(port_ledbar, 1)
grovepi.pinMode(port_ledbar, "OUTPUT")

# Constant settings
range_max = 30              # Max range
ledbar_nof_levels = 10      # Number of LEDs
lvl = 0                     # Starting level

# Continuously run the following:
while True:
    dist = grovepi.ultrasonicRead(port_ranger)  # Measure distance

    # Find the appropriate number of LEDs, set to 0 if out of range.
    if dist <= range_max:
        lvl = int((range_max - dist)/(range_max/ledbar_nof_levels))
    else:
        lvl = 0

    # Set the LEDs
    if 0 <= lvl <= ledbar_nof_levels:
        grovepi.ledBar_setLevel(port_ledbar, lvl)

    print(lvl, "<->", dist)

