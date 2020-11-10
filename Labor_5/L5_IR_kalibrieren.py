# Labor 5, Regelkreis, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-22
# organization:   HSLU T&A

## Import Packages
import time
import grovepi
import pigpio

## Main body
pi1 = pigpio.pi()   # Objekt der Klasse pi erstellen

# Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5         # Reference voltage of ADC is 5v
grove_vcc = 5       # Vcc of the grove interface is normally 5v
sensor_value = 0    # Initialwert, Variable fuer Abstandserkennung

x = 65               # Maximaldistanz in mm zur Aufnahme der Kalibrierkennlinie

# Pin Zuordnung
A1 = 20             # Anschluss M1
A2 = 21             # Anschluss M2
D2 = 26             # N/ -> Schaltet die Motortreiber A A/ ein

# Save results in CSV File
csvresult = open("/home/stud/mech/sensorkalibrierung.csv", "a")  # Allenfalls ist ein entsprechender Ordner zu erstellen
csvresult.write("Spannung (V);Abstand (mm)" + "\n")
csvresult.close

try:
    # Kalibrierkennlinie aufnehmen in 5 mm Schritten
    while x > 25:        # Minimaldistanz in mm,
        ausgabe = "Fahre auf " + str(x) + " mm  (Mit Enter bestaetigen)"
        eingabe = input(ausgabe)
        i = 0
        voltage_average = 0
        while i < 200:
            # Read sensor value
            sensor_value = grovepi.analogRead(sensor)

            # Calculate voltage
            voltage = round((float)(sensor_value) * adc_ref / 1024, 2)
            voltage_average += voltage
            i += 1

        v = voltage_average / i
        # print("sensor_value =", sensor_value, " voltage =", voltage)
        print(" voltage =", v)

        # Save results in CSV file
        csvresult = open("/home/stud/mech/sensorkalibrierung.csv", "a")
        csvresult.write(str(v) + ";" + str(x) + "\n")
        csvresult.close

        # Turn on Motor
        pi1.write(D2, 1)
        pi1.write(A1, 1)
        pi1.write(A2, 0)

        # Wait
        time.sleep(0.33)        # Einschaltzeit des Motors in s => entspricht ca. 5 mm Verfahrweg

        # Turn off motor
        pi1.write(D2, 0)
        # Kanalen A ausschalten
        pi1.write(A1, 0)
        pi1.write(A2, 0)

        # Change loop variable, around 5 mm moved.
        x = x - 5

except KeyboardInterrupt:
    pass

# Turn off motor
pi1.write(D2, 0)
# Kanalen A ausschalten
pi1.write(A1, 0)
pi1.write(A2, 0)
