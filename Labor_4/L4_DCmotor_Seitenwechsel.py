# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time

## Main Body
pi1 = pigpio.pi()   # Erstellt ein Objekt der Klasse pi
t_ein = 2           # Dauer des eingeschaltenen Motors

# Pin Zuordnung
A1 = 20  # A  oder M1
A2 = 21  # A/ oder M2
D2 = 26  # N/ -> Schaltet die Motortreiber A A/ ein

# Motortreiber einschalten -> 1
pi1.write(D2, 1)

print("Press Ctrl+C to interrupt")

try:
    while True:             # Endlosschleife
        pi1.write(A1, 1)    # Schaltet A1 ein
        pi1.write(A2, 0)    # Schaltet A2 aus
        time.sleep(t_ein)   # Motor fuer t_ein eingeschalten

        pi1.write(A1, 0)
        pi1.write(A2, 1)
        time.sleep(t_ein)   # Motor fuer t_ein ausgeschalten

except KeyboardInterrupt:
    pass

# Motortreiber ausschalten -> 0
pi1.write(D2, 0)
# A ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
