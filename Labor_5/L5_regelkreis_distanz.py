""" Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-22
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import pigpio
import signal
import time
from Motor_Off import Motor_Off
import grovepi
import os

""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of Motor,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    Motor_Off.turn_motor_off()          # Turn off DCmotor
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Initialize Grovepi
pi1 = pigpio.pi()   # Creates an Object from pi-class.

# Set ports
sensor = 0  # Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
A1 = 20     # A  or M1
A2 = 21     # A/ or M2
D2 = 26     # N/ -> Turn on the motordriver A A/

# Setup Sensor
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5 [V]
grove_vcc = 5       # Vcc of the grove interface is normally 5 [V]
sensor_value = 0    # Initial sensor value


""" Settings """
# Amplification factor k [s/mm]
k = 0.001               # Standard 0.001
# Velocity [%]
velocity = 0.80         # Standard = 0.80 [80%]
# Number of distance measurements [] over which to average
nmeasurement = 10       # Standard = 10


""" Initialize """
# Set speed by means of the pwm Duty cycle, between 0 und 255
dutycycle = int(velocity*255)

# Ask for the Set-distance
userinput = input("Auf welche Distanz soll gefahren werden?\nWert zwischen 30 mm und 60 mm: ")
set_distance = float(userinput)

# Save results in CSV File
filename = "/home/stud/Desktop/wegdiagramm_distanz" \
           + str(time.asctime(time.localtime(time.time()))).replace(":", "_") \
           + ".csv"
csvresult = open(filename, "w")                                 # Open and (over-)write ("w") file
csvresult.write("k= " + str(k) + "velocity= " + str(velocity) + "nmeasurement= " + str(nmeasurement)
                + "set_distance= " + str(set_distance) + "; " + "\n")     # Write set constants
csvresult.write("time (s); ist_distanz (mm)" + "\n")  # Write titles
csvresult.close()                                               # Close file

# Set time to 0
currenttime = 0


""" Control loop """
try:
    while True:
        # Reset values
        i = 0
        sensor_value_total = 0
        starttime = time.time()


        """ Measure distance """
        try:
            while i < nmeasurement:                         # For required measurements
                # Read sensor value
                sensor_value = grovepi.analogRead(sensor)
                sensor_value_total += sensor_value
                i += 1
        except KeyboardInterrupt:
            Motor_Off.turn_motor_off()
            pass

        # Find average voltage
        sensor_value_average = sensor_value_total / nmeasurement

        # Convert measurement to voltage
        voltage = round(float(sensor_value_average) * adc_ref / 1024, 4)

        # Calculate distance using sensor characteristics, coefficients found from calibration
        is_distance = round(44.593*voltage*voltage - 152.73*voltage + 159.38, 4)

        print("ist:   " + str(is_distance) + " mm")
        print("soll:  " + str(set_distance) + " mm")


        """ Compare current and set distance and set the motor accordingly """
        delta_distance = set_distance - is_distance     # Control error
        print("delta: " + str(delta_distance) + " mm")

        drivetime = delta_distance * k   # Multiply the found distance [mm] with the amplification k [s/mm]
        drivetime = abs(drivetime)      # Drivetime [s] is always positive

        print("t_ein: " + str(round(drivetime, 4)) + " s")


        """ Drive the motor for the calculated time """
        # Turn on the motordriver -> 1
        pi1.write(D2, 1)
        # Set PWM depending on direction of rotation
        if delta_distance > 0:
            pi1.set_PWM_frequency(A1, 4000)
            pi1.set_PWM_dutycycle(A1, dutycycle)  # PWM from 0 (OFF) to 255 (FULLY ON)
            pi1.write(A2, 0)

        if delta_distance < 0:
            pi1.write(A1, 0)
            pi1.set_PWM_frequency(A2, 4000)
            pi1.set_PWM_dutycycle(A2, dutycycle)  # PWM from 0 (OFF) to 255 (FULLY ON)

        time.sleep(drivetime)  # Drive for calculated drivetime


        """ Save position and time """
        csvresult = open(filename, "a")                 # Open and append ("a") file
        csvresult.write(str(round(currenttime, 4)) + ";" + str(round(is_distance, 4)) + "\n")  # Write one line of data
        csvresult.close()                               # Close the file


        """ Measure elapsed time """
        elapsed = time.time() - starttime       # Find elapsed time
        currenttime += elapsed                         # Update current time

except KeyboardInterrupt:
    pass
# Turn off DCmotor
Motor_Off.turn_motor_off()
