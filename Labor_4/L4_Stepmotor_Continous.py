# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

## Import Packages
import pigpio
import time


## Main Body
pi1 = pigpio.pi()   # Erstellt ein Objekt der Klasse pi
steptime = 0.001    # Wartezeit in Sekunden bis zum naechsten Step (Standard 0.001

# Pin Zuordnung
A1 = 20     # A  oder M1
A2 = 21     # A/ oder M2
B1 = 6      # B  oder M3
B2 = 13     # B/ oder M4
D1 = 12     # N  -> Schaltet die Motortreiber B B/ ein
D2 = 26     # N/ -> Schaltet die Motortreiber A A/ ein

# Motortreiber einschalten -> 1
# TODO um die Motortreiber einzuschalten, muss die Wert fur D1 und D2 1 sein.
pi1.write(D1, 0)
pi1.write(D2, 0)

print("Press Ctrl+C to interrupt")

try:
    while True:                 # Endlosschleife
        pi1.write(B1, 1)        # Schaltet B ein
        pi1.write(B2, 0)        # Schaltet B/ aus
        time.sleep(steptime)    # Wartezeit in Sekunden bis zum naechsten Step

        pi1.write(A1, 0)        # Schaltet A aus
        pi1.write(A2, 1)        # Schaltet A/ ein
        time.sleep(steptime)    # Wartezeit in Sekunden bis zum naechsten Step

        pi1.write(B1, 0)        # Schaltet B aus
        pi1.write(B2, 1)        # Schaltet B/ ein
        time.sleep(steptime)    # Wartezeit in Sekunden bis zum naechsten Step

        pi1.write(A1, 1)        # Schaltet A ein
        pi1.write(A2, 0)        # Schaltet A/ aus
        time.sleep(steptime)    # Wartezeit in Sekunden bis zum naechsten Step

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
