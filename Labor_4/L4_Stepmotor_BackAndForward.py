""" Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-06
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time
import grovepi
import signal
from Motor_Off import Motor_Off


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of Motor,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    Motor_Off.turn_motor_off()          # Turn off Stepmotor
    os._exit(0)

# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Initialize Grovepi
pi1 = pigpio.pi()   # Creates an Object from pi-class.

# Set ports
sensor = 0              # Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
A1 = 20 				# A  or M1
A2 = 21  				# A/ or M2
B1 = 6  				# B  or M3
B2 = 13 				# B/ or M4
D1 = 12                 # N  -> Turn on the motordriver B B/
D2 = 26                 # N/ -> Turn on the motordriver A A/

# Setup Sensor
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5 [V]
grove_vcc = 5       # Vcc of the grove interface is normally 5 [V]
sensor_value = 0    # Initial sensor value

# Settings
stoptime = 1        # Pause [s] between driving back and forth
steptime = 0.001    # Time [s] for each step of stepmotor. In fact sets motor speed.
step_number = 9600  # Number of steps [] to drive
sensor_min = 250    # minimal sensor value [*10 mm]
sensor_max = 270    # maximal sensor value [*10 mm]


""" Set the object at the right distance """
# while the position is outside this region:
while sensor_value < sensor_min or sensor_value > sensor_max:
    # Ask for any user input to continue
    print("Fahren Sie den Schlitten auf 15.0 mm!")
    userinput = input("Ready? (Press Enter)")
    # Read and print sensor output
    sensor_value = grovepi.analogRead(sensor)
    print("Abstand betraegt: ", sensor_value)


""" Endless loop """
print("Start Event Log ...")
print("Press Ctrl+C to interrupt")
try:
    while True:
        # Turn on Motordriver -> 1
        pi1.write(D1, 1)
        pi1.write(D2, 1)

        i = 0              # Set step counter
        while i < step_number:      # run one direction for step_number steps
            # one cycle consists of 4 steps:
            pi1.write(B1, 1)
            pi1.write(B2, 0)
            time.sleep(steptime)
            i += 1                  # Index +1

            pi1.write(A1, 0)
            pi1.write(A2, 1)
            time.sleep(steptime)
            i += 1

            pi1.write(B1, 0)
            pi1.write(B2, 1)
            time.sleep(steptime)
            i += 1

            pi1.write(A1, 1)
            pi1.write(A2, 0)
            time.sleep(steptime)
            i += 1

        time.sleep(stoptime)    # Wait for set time

        i = 0                   # Reset step counter
        while i < step_number:      # run the other direction for step_number steps
            # one cycle consists of 4 steps:
            pi1.write(A1, 1)
            pi1.write(A2, 0)
            time.sleep(steptime)
            i += 1                  # Index +1

            pi1.write(B1, 0)
            pi1.write(B2, 1)
            time.sleep(steptime)
            i += 1

            pi1.write(A1, 0)
            pi1.write(A2, 1)
            time.sleep(steptime)
            i += 1

            pi1.write(B1, 1)
            pi1.write(B2, 0)
            time.sleep(steptime)
            i += 1

        # Turn off stepmotor
        turn_motor_off()

        # Ask for any user input to continue
        userinput = input("Messung wiederholen? (Press Enter for yes)")

except KeyboardInterrupt:
    Motor_Off.turn_motor_off()          # Turn off Stepmotor
    pass
