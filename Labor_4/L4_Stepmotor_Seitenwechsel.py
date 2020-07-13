# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time


## Main Body
pi1 = pigpio.pi()
steptime = 0.001        # Wartezeit in Sekunden bis zum naechsten Step

# Pin Zuordnung
A1 = 20 				# A  oder M1
A2 = 21  				# A/ oder M2
B1 = 6  				# B  oder M3
B2 = 13 				# B/ oder M4
D1 = 12                 # N  -> Schaltet die Motortreiber B B/ ein
D2 = 26                 # N/ -> Schaltet die Motortreiber A A/ ein

try:
    while True:     # Endlosschleife
        eingabe = raw_input("Richtung waehlen ([r] rueckwaerts / [v] vorwaerts: ")
        print("Mit Ctrl + C beenden")
      
        if eingabe == 'v':
            # Motortreiber einschalten -> 1
            pi1.write(D1, 1)
            pi1.write(D2, 1)

            try: 
                while True:             # Endlosschleife
                    pi1.write(B1, 1)
                    pi1.write(B2, 0)
                    time.sleep(steptime)

                    pi1.write(A1, 0)
                    pi1.write(A2, 1)
                    time.sleep(steptime)

                    pi1.write(B1, 0)
                    pi1.write(B2, 1)
                    time.sleep(steptime)

                    pi1.write(A1, 1)
                    pi1.write(A2, 0)
                    time.sleep(steptime)
            except KeyboardInterrupt:
                pass

        if eingabe == 'r':
            # Motortreiber einschalten -> 1
            pi1.write(D1, 1)
            pi1.write(D2, 1)

            try: 
                while True:             # Endlosschleife
                    pi1.write(A1, 1)
                    pi1.write(A2, 0)
                    time.sleep(steptime)

                    pi1.write(B1, 0)
                    pi1.write(B2, 1)
                    time.sleep(steptime)

                    pi1.write(A1, 0)
                    pi1.write(A2, 1)
                    time.sleep(steptime)

                    pi1.write(B1, 1)
                    pi1.write(B2, 0)
                    time.sleep(steptime)

            except KeyboardInterrupt:
                pass

       # Motortreiber ausschalten -> 0
        pi1.write(D1, 0)
        pi1.write(D2, 0)

except KeyboardInterrupt:
    pass

#Motortreiber ausschalten -> 0
pi1.write(D1, 0)
pi1.write(D2, 0)
# A und B ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
pi1.write(B1, 0)
pi1.write(B2, 0)
