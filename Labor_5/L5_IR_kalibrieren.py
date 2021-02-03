""" Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-22
    organization:   HSLU T&A """

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ausgefuehrt werden: sudo pigpiod

## Import Packages
import pigpio
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
    turn_motor_off()          # Turn off DCmotor
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

# Settings
xmax = 65                       # Maximum distance [mm]
xmin = 25                       # Minimal distance [mm]
nmeasurement = int((65-25)/5 + 1)   # Number of measurements for each measurement cycle []
ncycle = 2                     # Number of measurement cycles []


""" Save results in CSV File """
filename = "/home/stud/mech/" + "sensorkalibrierung.csv"    # The filename can be edited
csvresult = open(filename, "w")                             # Open and (over-)write ("w") file
csvresult.write("Spannung (V); Abstand (mm)" + "\n")         # Write titles
csvresult.close                                             # Close file


""" Measure and Save data """
x = xmax                # Set x to the maximum distance
towards_sensor = True   # Start with moving towards sensor.
try:
    for measurement in range(nmeasurement*ncycle):   # Loop over all measurements
        # Ask user to drive to the current measurement distance
        userinput = "Fahre auf " + str(x) + " mm  (Mit Enter bestaetigen)"
        userinput = input(userinput)


        """ Measure distance """
        i = 0                   # Reset counter
        voltage_average = 0     # Reset average Voltage
        while i < 200:          # For 200 measurements
            # Read sensor value
            sensor_value = grovepi.analogRead(sensor)

            # Calculate voltage and add to average
            voltage = round((float)(sensor_value) * adc_ref / 1024, 2)
            voltage_average += voltage
            i += 1

        # Find and print average
        v = voltage_average / i
        print(" voltage =", v)


        """ Save measurement to CSV """
        csvresult = open(filename, "a")                 # Open and append ("a") file
        csvresult.write(str(v) + "; " + str(x) + "\n")  # Write one line of data
        csvresult.close                                 # Close the file


        """ Update distance """
        # Change loop variable, 5 mm moved.
        if towards_sensor:      # When moving toward sensor
            if x > xmin:        # When minimal distance is not reached yet:
                x -= 5          # Move 5 [mm] closer
            elif x == xmin:     # When minimal distance is reached:
                x = x           # 2nd point at minimal distance
                towards_sensor = False    # Start moving away from sensor
        else:                   # When not moving toward sensor
            if x < xmax:        # When maximal distance is not reached yet:
                x += 5          # Move 5 [mm] away
            elif x == xmax:     # When maximal distance is reached:
                x = x           # 2nd point at maximal distance
                towards_sensor = True     # Start moving towards sensor

except KeyboardInterrupt:
    pass
# Turn off DCmotor
turn_motor_off()
