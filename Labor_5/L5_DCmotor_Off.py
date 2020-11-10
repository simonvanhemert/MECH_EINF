# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time

## Main Body
pi1 = pigpio.pi()       # Erstellt ein Objekt der Klasse pi
waittime = 0.01         # Pause im Programmcode, um das Einlesen des KeyboardInterrupt zu ermoeglichen

# Pin Zuordnung
A1 = 20 	# A  oder M1
A2 = 21  	# A/ oder M2
D2 = 26     # N/ -> Schaltet die Motortreiber A A/ ein

# Motortreiber einschalten -> 1
pi1.write(D2, 1)

print("Press Ctrl+C to interrupt")

pi1.write(A1, 0)  # Schaltet A1 aus
pi1.write(A2, 0)  # Schaltet A2 aus
time.sleep(waittime)

# Motortreiber ausschalten -> 0
pi1.write(D2, 0)
