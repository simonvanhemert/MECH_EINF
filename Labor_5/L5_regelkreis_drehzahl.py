# Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-22
# organization:   HSLU T&A

## Import Packages
import pigpio
import time
import grovepi

## Main body
pi1 = pigpio.pi()   # Objekt der Klasse pi erstellen

# IR-Sensorsensor konfigurieren
sensor = 0
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5v
sensor_value = 0    # Initialwert, Variable fuer Abstandserkennung

# Pin Zuordnung
A1 = 20     # Anschluss M1
A2 = 21     # Anschluss M2
D2 = 26     # N/ -> Schaltet die Motortreiber A A/ ein


""" Einstellungen """
# Verstaerkungsfaktor
k = 5                   # Standard 5
# Anzahl Distanzmessungen [] über welche der Mittelwert genommen wird
anzahlmessungen = 10    # Standard = 10
# Wartezeit Zwischen Regelpunkte [s]
t_wart = 0.5            # Standard = 0.5
#  Offset zu ausgegebenen [12V / 255] geschwindigkeit, in bereich 0 - 255
offset = 10             # Standard = 10


""" Initialisierung """
# Eingabe soll-Distanz
eingabe = input("Auf welche Distanz soll gefahren werden?\nWert zwischen 30 und 60 mm: ")
soll_distanz = float(eingabe)

# Save results to CSV file, write titles
datei = "/home/stud/mech/wegdiagramm_drehzahl" + str(time.asctime(time.localtime(time.time()))).replace(":", "_") + ".csv"
csvresult = open(datei, "w")
csvresult.write("time (s)" + ", " + "ist_distanz (mm)" + "\n")
csvresult.close()

zeit = 0


""" Endlosschleife """
try:
    while True:
        # Reset values
        i = 0
        sensor_value_total = 0
        starttime = time.time()


        """ Ab hier wird der Abstand gemessen """
        while i < anzahlmessungen:
            # Read sensor value
            sensor_value = grovepi.analogRead(sensor)  # Einlesen IR-Sensor
            sensor_value_total += sensor_value
            i += 1

        # Durchschnittswert ueber die letzten i Messwerte
        sensor_value_average = sensor_value_total / anzahlmessungen

        # Distanz wird berechnet anhand der Kalibrierungskennlinie
        voltage = round(float(sensor_value_average) * adc_ref / 1024, 4)
        # Koeffizienten gemaess polynomischer Trendlinie (Excel)
        ist_distanz = round(44.593*voltage*voltage - 152.73*voltage + 159.38, 4)

        print("ist:  " + str(ist_distanz) + " mm")
        print("soll: " + str(soll_distanz) + " mm")


        """ Ab hier wird die ist-Distanz mit der soll-Distanz verglichen, und die Regler eingestellt """
        delta_distanz = soll_distanz - ist_distanz  # Regelabweichung
        print("delta: " + str(delta_distanz) + " mm")

        y = delta_distanz * k   # Multiplizieren mit Verstaerkungsfaktor

        # Geschwindigkeit einstellen durch Duty cycle, zwischen 0 und 255
        dutycycle = int(abs(y) + offset)
        if dutycycle < 0:
            dutycycle = 0
        if dutycycle > 255:
            dutycycle = 255



        """ Ab hier wird die motor angesteuert """
        # Motortreiber einschalten -> 1
        pi1.write(D2, 1)
        # Entscheidet in welche Richtung
        if y > 0:
            pi1.set_PWM_frequency(A1, 4000)
            pi1.set_PWM_dutycycle(A1, dutycycle)  # PWM from 0 (OFF) to 255 (FULLY ON)
            pi1.write(A2, 0)

        if y < 0:
            pi1.write(A1, 0)
            pi1.set_PWM_frequency(A2, 4000)
            pi1.set_PWM_dutycycle(A2, dutycycle)  # PWM from 0 (OFF) to 255 (FULLY ON)

        time.sleep(t_wart)      # Pause mit gegebener Laenge


        """ Ab hier werden die Zeit und der Position gespeichert """
        # Save results to CSV file
        csvresult = open(datei, "a")
        csvresult.write(str(round(zeit, 4)) + "," + str(round(ist_distanz, 4)) + "\n")
        csvresult.close()


        """ Zeit Messung wird durchgeführt und die Zeit wir angepasst"""
        elapsed = time.time() - starttime
        zeit += elapsed

except KeyboardInterrupt:
    pass

# Motortreiber ausschalten -> 0
pi1.write(D2, 0)
# Kanalen A ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
