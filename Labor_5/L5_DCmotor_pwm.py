# Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-22
# organization:   HSLU T&A

## Import Packages
import pigpio
import time

## Main body
pi1 = pigpio.pi()                       # Objekt der Klasse pi erstellen

# Pin Zuordnung
A1 = 20                                 # Anschluss M1
A2 = 21                                 # Anschluss M2
D2 = 26                                 # N/ -> Schaltet die Motortreiber A A/ ein

# Parameter definieren
voltage = 6                             # Gewuenschte Spannung fuer Motor zwischen 0 und 12 V eingeben (Speisespannung am Labornetzgeraet auf 12V einstellen)
dutycycle = round(21.25 * voltage, 0)   # Umrechnung PWM von 0 (OFF) auf 255 bit (FULLY ON)
laufzeit = 1                            # Laufzeit in sekunden

# Motortreiber einschalten -> 1
pi1.write(D2, 1)
    
# Richtung bestimmen mit gewaehlten Ausgaengen
pi1.set_PWM_frequency(A1, 4000)         # Frequenz des PWM Signals in Hz -> 4000
pi1.set_PWM_dutycycle(A1, dutycycle)
pi1.write(A2, 0)

time.sleep(laufzeit)                    # Dauer der Einschaltzeit in s

# Motortreiber ausschalten -> 0
pi1.write(D2, 0)
# Kanalen A ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
