""" Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-22
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import grovepi
import signal
import time


""" Initialization """
def receiveSignal(signalNumber, frame):
    """ When any error signal is received:
    - print signal number,
    - turn of Motor,
    - and exit """
    print("Received: ", signalNumber)
    print("Exit Python!")
    os._exit(0)


# When a signal is received, activate the (above) receiveSignal method.
signal.signal(signal.SIGINT, receiveSignal)

# Set ports
sensor = 0  # Connect the Grove 80cm Infrared Proximity Sensor to analog port A0

# Setup Sensor
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5 [V]
grove_vcc = 5       # Vcc of the grove interface is normally 5 [V]
sensor_value = 0    # Initial sensor value


""" Measure distance"""
try:
    while True:
        i = 0                   # Reset counter
        voltage_average = 0     # Reset average Voltage
        while i < 100:          # For 100 measurements
            # Read sensor value
            sensor_value = grovepi.analogRead(sensor)

            # Calculate voltage and add to average
            voltage = round((float)(sensor_value) * adc_ref / 1024, 2)
            voltage_average += voltage
            i += 1

        # Find average voltage
        v = voltage_average / i

        # Calculate distance using sensor characteristics, coefficients found from calibration
        is_distance = round(44.593*voltage*voltage - 152.73*voltage + 159.38, 2)

        # Print output and pause
        print("Spannung ist", voltage, "\nDistanz ist: " + str(is_distance) + " mm")
        time.sleep(0.5)

except KeyboardInterrupt:
    pass

