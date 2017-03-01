#!/usr/bin/env python3
# This script can be run from Brickman
# I found a lot of help on:
# https://sites.google.com/site/ev3python/learn_ev3_python

from ev3dev.ev3 import *
from time   import sleep
from ColorConversion import rgb2hsv
# Konstante
Ts=0.04
kor=0.02
speed = 12/Ts
slabljenje= 0.5

#to je komentar


# Set up the motor ports

mR = LargeMotor('outA')
mL = LargeMotor('outC') #B port is somehow not working
mS = MediumMotor('outD') #Sensor which turns the ultrasonic sensor

# Set up the ultrasonic senso
us = UltrasonicSensor() 
assert us.connected, "Connect a single US sensor to any sensor port"
us.mode='US-DIST-CM'
units = us.units

# Set up the color sensor
cl = ColorSensor() 
assert cl.connected, "Connect a single EV3 color sensor to any sensor port"
cl.mode='RGB-RAW'
# Set up the gyro sensor


course = 0 #start direction. when it is positive program is turning right
last_black=0
last_white=0

start = time.time()
tmax = start


try:
    while us.value()>45: #not ts.value():    # Stop program by pressing touch sensor button
        # Meritev maksimalnega casa ki ga zanka porabi da se izvede
        tmp = time.time() - start
        if tmp<tmax:
            tmax=tmp
        start = start+tmp
                
        # za doseganje konstantne frekvence vzorcenja
        #start = start + Ts
        #while 0<(time.time()-start): 
        #    sleep(0.0001)
        #print(str(start))

        #Branje Color Senzorja in sledenje barvnemu traku
        red = cl.value(0)
        green=cl.value(1)
        blue=cl.value(2)
        
        #print("Red: " + str(red) + ", Green: " + str(green) + ", Blue: " + str(blue))
        [H, S, V] = rgb2hsv(red, green, blue)
        #print("H: " + str(H) + ", S: " + str(S) + ", V: " + str(V))
        last_black=last_black+1
        last_white=last_white+1

        if V<0.65:
            course = course + kor/(abs(course)+0.1)
            last_black=0
        elif V> 1.42:
            if last_black<(0.2/(Ts)):
                course = course + 2*kor/(abs(course)+0.1)
            else:
                course = course - kor/(abs(course)+0.1)
            
            last_white=0

        else:
            course=course*slabljenje

            
        Lspeed=(1+course)*speed
        Rspeed=(1-course)*speed

        if Lspeed>1000:
            Lspeed=1000
        elif Lspeed<-1000:
            Lspeed=-1000
        

        if Rspeed>1000:
            Rspeed=1000
        elif Rspeed<-1000:
            Rspeed=-1000

        
        mL.run_forever( speed_sp=Lspeed)
        mR.run_forever( speed_sp=Rspeed)

except KeyboardInterrupt:
    pass
#Sound.beep()
mL.stop()
mR.stop()
