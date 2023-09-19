# spot-robot


## Pre requisites

i2c must be enable throughpi-config

# For gyro test
sudo apt-get install python3-opengl freeglut3-dev 
python3 -m pip install PyOpenGL PyOpenGL_accelerate

Then ssh -X ...


apt install python3-smbus


pip3 install -r requirements.txt

Add ubuntu user to i2c group
usermod -a -G i2c ubuntu
usermod -a -G input ubuntu
usermod -a -G kmem ubuntu
chmod g+w /dev/mem


pip3 install adafruit-circuitpython-servokit

Build and run
python3 src/gyro.py
python3 src/spot.py



