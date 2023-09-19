from http.server import BaseHTTPRequestHandler, HTTPServer
from mpu6050 import mpu6050
from math import atan2

import threading

from time import sleep, time


gyro_front = 0.
gyro_side = 0.
gyro_time = 0.
gyro_lock = threading.Lock()


 
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
                    gyro_front=round(sum(front_accel_sorted[3:7])/len((front_accel_sorted[3:7])) + GYRO_CORR_FRONT, 2)
                    gyro_side=round(sum(side_accel_sorted[3:7])/len((side_accel_sorted[3:7])) + GYRO_CORR_SIDE, 2)
                    gyro_time=time()
                    if gyro_lock.locked():
                        gyro_lock.release()

                i=i+1

            except Exception:
                pass
                if gyro_lock.locked():
                    gyro_lock.release()



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global gyro_front, gyro_side, gyro_time, gyro_lock, all_run

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(str(gyro_front) + " " + str(gyro_side), 'utf-8'))

 

if __name__ == "__main__":
    # Create Gyro thread
    gyro_thread = threading.Thread(name='spotgyro', target=spotgyro)
    gyro_thread.setDaemon(True)
    gyro_thread.start()

    print("tutu")
    webServer = HTTPServer(('192.168.1.26', 8080), MyServer)
    print("Server started http://%s:%s" % ('192.168.1.26', 8080))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    print("tutu2")
