import web
from mpu6050 import mpu6050
from math import atan2

import threading

from time import sleep, time


gyro_front = 0.
gyro_side = 0.
gyro_time = 0.
gyro_lock = threading.Lock()
 

urls = (

    '/', 'index'

)

GYRO_CORR_FRONT=2.31
GYRO_CORR_SIDE=-1

all_run = True
 

def spotgyro():
    global gyro_front, gyro_side, gyro_time, gyro_lock, all_run

    while all_run:

        gyro=None

        while gyro == None:
            try:
                gyro=mpu6050(0x68)
            except:
                raise Exception("Could not connect to Gyroscope MPU6050")

            sleep(1)

        i=0
        front_accel=[0] * 10
        side_accel=[0] * 10

        print("TOTOT")

        while True:
            try:
                accelval = gyro.get_accel_data()
                front_accel[i] = atan2(accelval['x'],accelval['z'])*180/3.14159
                side_accel[i] = atan2(accelval['y'],accelval['z'])*180/3.14159

                if i == 9:
                    i=0
                    front_accel_sorted=sorted(front_accel, key=float)
                    side_accel_sorted=sorted(side_accel, key=float)
                    gyro_lock.acquire()
                    gyro_front=sum(front_accel_sorted[3:7])/len((front_accel_sorted[3:7])) + GYRO_CORR_FRONT
                    gyro_side=sum(side_accel_sorted[3:7])/len((side_accel_sorted[3:7])) + GYRO_CORR_SIDE
                    gyro_time=time()
                    print("updated: " + str(gyro_front) + " " + str(gyro_side))
                    if gyro_lock.locked():
                        gyro_lock.release()

                i=i+1

            except Exception:
                pass
                if gyro_lock.locked():
                    gyro_lock.release()



class index:
    def GET(self):
        global gyro_front, gyro_side, gyro_time, gyro_lock, all_run
        res = str(gyro_front) + " " + str(gyro_side)
        return res

 

if __name__ == "__main__":
    global gyro_front, gyro_side, gyro_time, gyro_lock, all_run
    # Create Gyro thread
    gyro_thread = threading.Thread(name='spotgyro', target=spotgyro)
    gyro_thread.setDaemon(True)
    gyro_thread.start()

    print("tutu")
    app = web.application(urls, globals())
    print("tutu2")
    app.run()
