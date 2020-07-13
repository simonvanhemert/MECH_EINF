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

# Infrarot Sensor konfigurieren
sensor = 0
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5 		# Reference voltage of ADC is 5v
sensor_value = 0 	# Variable fuer Abstandserkennung

# Pin Zuordnung
A1 = 20     # Anschluss M1
A2 = 21     # Anschluss M2
D2 = 26     # N/ -> Schaltet die Motortreiber A A/ ein

# Verstaerkungsfaktor
k = 0.01        # Standard 0.01

eingabe = input("Auf welche Distanz soll gefahren werden?\nWert zwischen 30 mm und 60 mm: ")
soll_distanz = float(eingabe)

# # Save results to CSV file, write titles
csvresult = open("/home/stud/mech/wegdiagramm_distanz.csv", "w")
csvresult.write("time (s)" + "ist_distanz (mm)" + ", " + "\n")
csvresult.close

zeit = 0

try:
    while True:
        # Reset values
        i = 0
        sensor_value_total = 0
        starttime = time.time()

        while i < 10:
            # Read sensor value
            sensor_value = grovepi.analogRead(sensor)  # Einlesen Infrarotsensorwert
            sensor_value_total += sensor_value
            i += 1

        # Durchschnittswert ueber die letzten i Messwerte
        sensor_value_average = sensor_value_total / i

        # Distanz wird berechnet mit den Koeffizienten der Kalibrierungskennlinie des IR Sensors
        voltage = round(float(sensor_value_average) * adc_ref / 1024, 2)
        ist_distanz = round(??*voltage*voltage - ??*voltage + ??, 2)

        print("ist:   " + str(round(ist_distanz, 4)) + " mm")
        print("soll:  " + str(round(soll_distanz, 4)) + " mm")

        delta_distanz = soll_distanz - ist_distanz  # Regelabweichung

        print("delta: " + str(delta_distanz) + " mm")

        y = delta_distanz * k  # Multiplizieren mit Verstaerkungsfaktor, y gibt Vorzeichen fuer Drehrichtung an

        t_ein = abs(y)        # Einschaltzeit des Motors, Betrag von y

        print("t_ein: " + str(round(t_ein, 7)) + " s")
        print("Drehrichtung: " + str(round(y, 2)))

        # Motortreiber einschalten -> 1
        pi1.write(D2, 1)
        # entscheidet in welche Richtung
        if y > 0:
            pi1.write(A1, 0)        # 1
            pi1.write(A2, 1)        # 0

        if y < 0:
            pi1.write(A1, 1)        # 0
            pi1.write(A2, 0)        # 1

        time.sleep(t_ein)  # Pause mit berechneter Laenge
        print(" ")

        # Save results to CSV file
        csvresult = open("/home/stud/mech/wegdiagramm_distanz.csv", "a")
        csvresult.write(str(round(zeit, 4)) + "," + str(round(ist_distanz, 4)) + "\n")
        csvresult.close

        elapsed = time.time() - starttime
        zeit += elapsed

except KeyboardInterrupt:
    pass

# Motortreiber ausschalten -> 0
pi1.write(D2, 0)
# Kanalen A ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
