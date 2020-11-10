# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time
import grovepi

## Main Body
pi1 = pigpio.pi()
steptime = 0.001    # Wartezeit in Sekunden bis zum naechsten Step

# Pin Zuordnung
sensor = 0              # Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
A1 = 20 				# A  oder M1
A2 = 21  				# A/ oder M2
B1 = 6  				# B  oder M3
B2 = 13 				# B/ oder M4
D1 = 12                 # N  -> Schaltet die Motortreiber B B/ ein
D2 = 26                 # N/ -> Schaltet die Motortreiber A A/ ein

# Setup Sensor
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5v
grove_vcc = 5       # Vcc of the grove interface is normally 5v
sensor_value = 0    # Initial sensor value

# Set the object at the right distance
while sensor_value > 263 or sensor_value < 257:     # As long as the position is not good:
    print("Fahren Sie den Schlitten auf 15.0 mm!")
    eingabe = input("Ready? (Press Enter)")
    sensor_value = grovepi.analogRead(sensor)       # Read sensor value
    print("Abstand betraegt: ", sensor_value)

try:
    while True:             # Endlosschleife
        # Motortreiber einschalten -> 1
        pi1.write(D1, 1)
        pi1.write(D2, 1)

        i = 0               # Set index counter
        while i < 9600:    # run one way
            pi1.write(B1, 1)
            pi1.write(B2, 0)
            time.sleep(steptime)
            i += 1          # Index +1

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

        time.sleep(1)

        i = 0               # Reset index counter
        while i < 9600:    # Run the other way
            pi1.write(A1, 1)
            pi1.write(A2, 0)
            time.sleep(steptime)
            i += 1

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

        # Motortreiber ausschalten -> 0
        pi1.write(D1, 0)
        pi1.write(D2, 0)
        
        eingabe = input("Messung wiederholen? (Press Enter for yes)")

except KeyboardInterrupt:
    pass

# Motortreiber ausschalten -> 0
pi1.write(D1, 0)
pi1.write(D2, 0)
# A und B ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
pi1.write(B1, 0)
pi1.write(B2, 0)
