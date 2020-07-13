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

# Verstaerkungsfaktor
k = 0.1            # Standard 0.1

# Fuer Python 2 input = raw_input! for Python 3 input ist das richtige Kommando.
eingabe = input("Auf welche Distanz soll gefahren werden?\nWert zwischen 30 und 60 mm: ")
soll_distanz = float(eingabe)

# # Save results to CSV file, write titles
csvresult = open("/home/stud/mech/wegdiagramm_drehzahl.csv", "w")
csvresult.write("time (s)" + ", " + "ist_distanz (mm)" + "\n")
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
            sensor_value = grovepi.analogRead(sensor)  # Einlesen IR-Sensor
            sensor_value_total += sensor_value
            i += 1

        # Durchschnittswert ueber die letzten i Messwerte
        sensor_value_average = sensor_value_total / i

        # Distanz wird berechnet anhand der Kalibrierungskennlinie
        voltage = round(float(sensor_value_average) * adc_ref / 1024, 3)
        # ist_distanz = round(42.677*voltage*voltage - 147.75*voltage + 155.03, 2)
        ist_distanz = round(??*voltage*voltage - ??*voltage + ??, 2)

        print("ist:  " + str(ist_distanz) + " mm")
        print("soll: " + str(soll_distanz) + " mm")

        delta_distanz = soll_distanz - ist_distanz  # Differenz von soll und ist
        print("delta: " + str(delta_distanz) + " mm")

        y = delta_distanz * k   # Multiplizieren mit Verstaerkungsfaktor

        # Set Duty cycle, between 0 and 255
        dutycycle = int(abs(y) * 50 + 55)
        if dutycycle < 0:
            dutycycle = 0
        if dutycycle > 255:
            dutycycle = 255

        # Motortreiber einschalten -> 1
        pi1.write(D2, 1)
        # Entscheidet in welche Richtung
        if y < 0:
            pi1.set_PWM_frequency(A1, 4000)
            pi1.set_PWM_dutycycle(A1, dutycycle)  # PWM from 0 (OFF) to 255 (FULLY ON)
            pi1.write(A2, 0)

        if y > 0:
            pi1.write(A1, 0)
            pi1.set_PWM_frequency(A2, 4000)
            pi1.set_PWM_dutycycle(A2, dutycycle)  # PWM from 0 (OFF) to 255 (FULLY ON)

        time.sleep(0.5)
        print(" ")

        # # Save results to CSV file
        csvresult = open("/home/stud/mech/wegdiagramm_drehzahl.csv", "a")
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
