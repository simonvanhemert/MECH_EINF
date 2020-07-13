# coding=utf-8
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
adc_ref = 5         # Reference voltage of ADC is 5v
grove_vcc = 5       # Vcc of the grove interface is normally 5v
sensor_value = 0    # Initialwert, Variable fuer Abstandserkennung

try:
    while True:		# Durchschnittswert ueber die letzten i Messwerte
        i = 0
        sensor_value_total = 0
        while i < 100:
            # Read sensor value
            sensor_value = grovepi.analogRead(sensor)       # Einlesen Infrarotsensorwert
            sensor_value_total += sensor_value
            i += 1

        # Durchschnittswert ueber die letzten 100 Messwerte
        sensor_value_average = sensor_value_total / i

        # measured voltage
        voltage = round(float(sensor_value_average) * adc_ref / 1024, 3)

        # Distanz wird berechnet mit den Koeffizienten der Kalibrierungskennline des IR Sensors
        ist_distanz = round(??*voltage*voltage - ??*voltage + ??, 2)    # Koeffizienten gemaess polynomischer Trendlinie (Excel)
 
        print("ist: " + str(ist_distanz) + " mm")
        time.sleep(1)

except KeyboardInterrupt:
    pass

