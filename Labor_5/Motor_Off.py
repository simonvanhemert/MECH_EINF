""" Labor 4, Umkehrspiel, MECH_EINF Module WI HSLU T&A
    author:         Simon van Hemert
    date:           2020-04-06
    organization:   HSLU T&A """

## Import Packages
import pigpio

class Motor_Off:
    """ Class to correctly turn of the DC motor oder Stepper motor """
    @staticmethod
    def turn_motor_off():
        """ Definition to turn of the motor driver channels and drivers """
        pi1 = pigpio.pi()       # Create an object of class pi

        # Set ports and settings
        A1 = 20 	# A  or M1
        A2 = 21  	# A/ or M2
        B1 = 6      # B  or M3
        B2 = 13     # B/ or M4
        D1 = 12     # N  -> Turn on the motordriver B B/
        D2 = 26     # N/ -> Turn on the motordriver A A/

        # Turn on Motordrivers -> 1
        pi1.write(D1, 1)
        pi1.write(D2, 1)

        # Set channels to 0
        pi1.write(A1, 0)
        pi1.write(A2, 0)
        pi1.write(B1, 0)
        pi1.write(B2, 0)

        # Turn off Motordrivers -> 0
        pi1.write(D1, 0)
        pi1.write(D2, 0)

        print("Motor turned off")


# When this program is run
if __name__ == '__main__':
    # run defined method to turn of the motor
    Motor_Off.turn_motor_off()
