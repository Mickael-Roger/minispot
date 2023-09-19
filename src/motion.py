import time
from adafruit_servokit import ServoKit

#Constants
nbPCAServo=16

#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

#Objects
pca = ServoKit(channels=16)


BACK_RIGHT_LEG=3
BACK_RIGHT_SHOULDER=1
BACK_RIGHT_FOOT=0

BACK_LEFT_LEG=14
BACK_LEFT_SHOULDER=12
BACK_LEFT_FOOT=13

FRONT_RIGHT_LEG=10
FRONT_RIGHT_SHOULDER=8
FRONT_RIGHT_FOOT=9

FRONT_LEFT_LEG=4
FRONT_LEFT_SHOULDER=5
FRONT_LEFT_FOOT=6




# function init 
def init():

    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])


# function main 
def main():

    pcaScenario();


# function pcaScenario 
def pcaScenario():
    """Scenario to test servo"""
    
    pca.servo[BACK_RIGHT_FOOT].angle = 90
    pca.servo[BACK_LEFT_FOOT].angle = 90
    pca.servo[FRONT_RIGHT_FOOT].angle = 90
    pca.servo[FRONT_LEFT_FOOT].angle = 90

    time.sleep(1)
    time.sleep(1)

    pca.servo[BACK_RIGHT_LEG].angle = 90
    pca.servo[BACK_LEFT_LEG].angle = 90
    pca.servo[FRONT_RIGHT_LEG].angle = 90
    pca.servo[FRONT_LEFT_LEG].angle = 90

    time.sleep(1)
    time.sleep(1)




if __name__ == '__main__':
    init()
    main()

