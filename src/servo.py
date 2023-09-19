from posix_ipc import MessageQueue
import json

from time import sleep

class Servo:

    def __init__(self):

        while True:
            try:
                self.mqservo = MessageQueue("/gyro")
                break
            except:
                sleep(1)
                pass

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        self.servos={'front_right_foot': {},
                     'front_right_leg': {},
                     'front_right_shoulder': {},
                     'front_left_foot': {},
                     'front_left_leg': {},
                     'front_left_shoulder': {},
                     'back_left_foot': {},
                     'back_left_leg': {},
                     'back_left_shoulder': {},
                     'back_right_foot': {},
                     'back_right_leg': {},
                     'back_right_shoulder': {},
                    }

        # Initialize Servos
        self.servos['front_right_foot']['servo']=GPIO.PWM(17, 50) 	# GPIO 17 for PWM with 50Hz
        self.servos['front_right_leg']['servo']=GPIO.PWM(17, 50)
        self.servos['front_right_shoulder']['servo']=GPIO.PWM(17, 50)
        self.servos['front_left_foot']['servo']=GPIO.PWM(17, 50)
        self.servos['front_left_leg']['servo']=GPIO.PWM(17, 50)
        self.servos['front_left_shoulder']['servo']=GPIO.PWM(17, 50)
        self.servos['back_left_foot']['servo']=GPIO.PWM(17, 50)
        self.servos['back_left_leg']['servo']=GPIO.PWM(17, 50)
        self.servos['back_left_shoulder']['servo']=GPIO.PWM(17, 50)
        self.servos['back_right_foot']['servo']=GPIO.PWM(17, 50)
        self.servos['back_right_leg']['servo']=GPIO.PWM(17, 50)
        self.servos['back_right_shoulder']['servo']=GPIO.PWM(17, 50)


        # Initialize Servos correction
        self.servos['front_right_foot']['correction']=0
        self.servos['front_right_leg']['correction']=0
        self.servos['front_right_shoulder']['correction']=0
        self.servos['front_left_foot']['correction']=0
        self.servos['front_left_leg']['correction']=0
        self.servos['front_left_shoulder']['correction']=0
        self.servos['back_left_foot']['correction']=0
        self.servos['back_left_leg']['correction']=0
        self.servos['back_left_shoulder']['correction']=0
        self.servos['back_right_foot']['correction']=0
        self.servos['back_right_leg']['correction']=0
        self.servos['back_right_shoulder']['correction']=0


        # Initialize Servos position
        self.servos['front_right_foot']['position']=0
        self.servos['front_right_leg']['position']=0
        self.servos['front_right_shoulder']['position']=0
        self.servos['front_left_foot']['position']=0
        self.servos['front_left_leg']['position']=0
        self.servos['front_left_shoulder']['position']=0
        self.servos['back_left_foot']['position']=0
        self.servos['back_left_leg']['position']=0
        self.servos['back_left_shoulder']['position']=0
        self.servos['back_right_foot']['position']=0
        self.servos['back_right_leg']['position']=0
        self.servos['back_right_shoulder']['position']=0


    def position(self, servo, position):

        if position > 180:
            position=180
        if position < 0:
            position=0

        if servo in ['front_left_foot', 'back_left_foot', 'front_right_leg', 'back_right_leg', 'front_right_shoulder', 'back_left_shoulder']:
            position=180-position

        if servo in self.servos:
            while self.servos[servo]['position'] != position:
                if position > self.servos[servo]['position']:
                    if position - self.servos[servo]['position'] > 5:
                        newpos=self.servos[servo]['position']+5
                    else:
                        newpos=position
                elif position < self.servos[servo]['position']:
                    if self.servos[servo]['position'] - position > 5:
                        newpos=self.servos[servo]['position']-5
                    else:
                        newpos=position

            pwm=2.5+(newpos*10/180)+(self.servos[servo]['correction']*10/180)
            self.servos[servo]['servo'].ChangeDutyCycle(pwm)
            self.servos[servo]['position']=newpos
            sleep(0.05)




    def start(self):
        while True:
            try:
                msg = self.mqservo.receive()
                msgvalues=json.loads(msg[0])
                self.position(msgvalues['servo'], int(msgvalues['position']))
            except:
                pass


if __name__ == '__main__':
    servo=Servo()
    servo.start()
