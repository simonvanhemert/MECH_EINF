# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time


## Main Body
pi1 = pigpio.pi() 		# Erstellt ein Objekt der Klasse pi
waittime = 0.01         # Pause im Programmcode, um das Einlesen des KeyboardInterrupt zu ermoeglichen

# Pin Zuordnung
A1 = 20 				# A  oder M1
A2 = 21  				# A/ oder M2
B1 = 6  				# B  oder M3
B2 = 13 				# B/ oder M4
D1 = 12                 # N  -> Schaltet die Motortreiber B B/ ein
D2 = 26                 # N/ -> Schaltet die Motortreiber A A/ ein

# Motortreiber einschalten -> 1
pi1.write(D1, 1)
pi1.write(D2, 1)

print("Press any key to interrupt...")

try:
    while True: 			    # Endlosschleife
        pi1.write(B1, 0) 		# Schaltet B aus
        pi1.write(B2, 0) 		# Schaltet B/ aus
        time.sleep(waittime) 	# Wartezeit in Sekunden bis zum naechsten Step

        pi1.write(A1, 0)		# Schaltet A aus
        pi1.write(A2, 0)		# Schaltet A/ aus
        time.sleep(waittime)    # Wartezeit in Sekunden bis zum naechsten Step

except KeyboardInterrupt:
    pass

# Motortreiber ausschalten -> 0
pi1.write(D1, 0)
pi1.write(D2, 0)
