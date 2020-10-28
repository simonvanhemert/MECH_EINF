# Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
# author:         Raphael Andonie, Simon van Hemert
# date:           2020-04-06
# organization:   HSLU T&A

# TODO !!! Vor dem eigentlichen Starten des Programmes muss zuerst folgender Befehl ohne Klammern ausgefuehrt werden (sudo pigpiod) !!!

## Import Packages
import pigpio
import time
import grovepi

## Main Body
pi1 = pigpio.pi()
steptime1 = 0.0005   	# Wartezeit in Sekunden bis zum naechsten Step, Vorwarts
steptime2 = 0.001    	# Wartezeit in Sekunden bis zum naechsten Step, Ruckwarts

# Pin Zuordnung
sensor = 0              # Connect the Grove 80cm Infrared Proximity Sensor to analog port A0
A1 = 20 				# A  oder M1
A2 = 21  				# A/ oder M2
B1 = 6  				# B  oder M3
B2 = 13 				# B/ oder M4
D1 = 12     			# N  -> Schaltet die Motortreiber B B/ ein
D2 = 26     			# N/ -> Schaltet die Motortreiber A A/ ein

# Setup Sensor
grovepi.pinMode(sensor, "INPUT")
adc_ref = 5        		# Reference voltage of ADC is 5v
grove_vcc = 5       	# Vcc of the grove interface is normally 5v
sensor_value = 0    	# Initial sensor value

# Verfahrweg vorwaerts
number_cycl = 5					# Anzahl cycles
steps_vor = 1600  				# 200 steps entsprechen 1 Umdrehung
steps_zur = 800	 				# 200 steps entsprechen 1 Umdrehung
steps_an_start = 5*steps_zur  	# Schlitten faehrt zurueck an die Ausgangsposition

# Set the object at the right distance
while sensor_value > 435 or sensor_value < 425:     # As long as the position is not good:
	print("Fahren Sie den Schlitten auf 15.0 mm!")
	eingabe = raw_input("Ready? (Press Enter)")
	sensor_value = grovepi.analogRead(sensor)       # Read sensor value
	print("Abstand betraegt: ", sensor_value)

try:
	while True:             # Endlosschleife
		# Motortreiber einschalten -> 1
		pi1.write(D1, 1)
		pi1.write(D2, 1)

		s = 0  					# Reset counter fur number of cycles
		while s < number_cycl:
			i = 0  # Faehrt vorwaerts fuer xy steps
			while i < steps_vor:
				pi1.write(B1, 1)
				pi1.write(B2, 0)
				time.sleep(steptime1)
				i += 1

				pi1.write(A1, 0)
				pi1.write(A2, 1)
				time.sleep(steptime1)
				i += 1

				pi1.write(B1, 0)
				pi1.write(B2, 1)
				time.sleep(steptime1)
				i += 1

				pi1.write(A1, 1)
				pi1.write(A2, 0)
				time.sleep(steptime1)
				i += 1

			i = 0  # Faehrt rueckwaerts fuer xy steps
			while i < steps_zur:
				pi1.write(A1, 1)
				pi1.write(A2, 0)
				time.sleep(steptime2)
				i += 1

				pi1.write(B1, 0)
				pi1.write(B2, 1)
				time.sleep(steptime2)
				i += 1

				pi1.write(A1, 0)
				pi1.write(A2, 1)
				time.sleep(steptime2)
				i += 1

				pi1.write(B1, 1)
				pi1.write(B2, 0)
				time.sleep(steptime2)
				i += 1

			print(i)
			s += 1

		j = 0  # Faehrt rueckwaerts fuer xy steps
		while j < steps_an_start:
			pi1.write(A1, 1)
			pi1.write(A2, 0)
			time.sleep(steptime2)
			j += 1

			pi1.write(B1, 0)
			pi1.write(B2, 1)
			time.sleep(steptime2)
			j += 1

			pi1.write(A1, 0)
			pi1.write(A2, 1)
			time.sleep(steptime2)
			j += 1

			pi1.write(B1, 1)
			pi1.write(B2, 0)
			time.sleep(steptime2)
			j += 1

		pi1.write(D1, 0)
		pi1.write(D2, 0)

		eingabe = raw_input("Messung wiederholen? (Press Enter for yes)")

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
