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
pi1 = pigpio.pi()   # Erstellt ein Objekt der Klasse pi
# waittime = 0.001    # Pause im Programmcode, um das Einlesen des KeyboardInterrupt zu ermoeglichen
drivetime = 2       # Fahrzeit
stoptime = 0.5      # Pause schwissen hin und her fahren

# Pin Zuordnung
sensor = 0              # Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
A1 = 20     # A  oder M1
A2 = 21     # A/ oder M2
D2 = 26     # N/ -> Schaltet die Motortreiber A A/ ein

# Setup Sensor
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5v
grove_vcc = 5       # Vcc of the grove interface is normally 5v
sensor_value = 0    # Initial sensor value

# Set the object at the right distance
while sensor_value > 263 or sensor_value < 258:     # As long as the position is not good: 435   425
    print("Fahren Sie den Schlitten auf 15.0 mm!")
    eingabe = raw_input("Ready? (Press Enter)")
    sensor_value = grovepi.analogRead(sensor)       # Read sensor value
    print("Abstand betraegt: ", sensor_value)

print("Press Ctrl+C to interrupt")

try:
    while True:                 # Endlosschleife
        # Motortreiber einschalten -> 1
        pi1.write(D2, 1)

        # Drive one way
        pi1.write(A1, 1)        # Schaltet A1 ein
        pi1.write(A2, 0)        # Schaltet A2 aus
        time.sleep(drivetime)    # Wartezeit in Sekunden

        # Motortreiber ausschalten -> 0
        pi1.write(D2, 0)
        time.sleep(stoptime)

        # Motortreiber einschalten -> 1
        pi1.write(D2, 1)

        # Drive other way
        pi1.write(A1, 0)  # Schaltet A1 ein
        pi1.write(A2, 1)  # Schaltet A2 aus
        time.sleep(drivetime)  # Wartezeit in Sekunden

        # Motortreiber ausschalten -> 0
        pi1.write(D2, 0)

        eingabe = raw_input("Messung wiederholen? (Press Enter for yes)")

except KeyboardInterrupt:
    pass

# Motortreiber ausschalten -> 0
pi1.write(D2, 0)
# Kanalen A ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
