#!/usr/bin/env python3
# so that script can be run from Brickman
# The following program was made by modifying examples from 
# https://sites.google.com/site/ev3python/learn_ev3_python

from ev3dev.ev3 import *
from time   import sleep

Ts=0.04
kor=0.02
speed = 12/Ts
slabljenje= 0.5

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


# Connect EV3 color sensor to any sensor port
# and check it is connected.



mL = LargeMotor('outC')
mR = LargeMotor('outA')

us = UltrasonicSensor() 
assert us.connected, "Connect a single US sensor to any sensor port"
# can have 2 statements on same line if use semi colon

# Put the US sensor into distance mode.
us.mode='US-DIST-CM'

units = us.units

cl = ColorSensor() 
assert cl.connected, "Connect a single EV3 color sensor to any sensor port"

# Connect touch sensor to any sensor port
# and check it is connected.

#ts = TouchSensor();  assert ts.connected, "Connect a touch sensor to any port"  
# you can have 2 statements on the same line if you use a semi colon

# Put the color sensor into RGB mode.
cl.mode='RGB-RAW'
start = time.time()
course = 0
last_black=0
last_white=0

#mL.run_forever(time_sp=3000, speed_sp=100)
#mR.run_forever(time_sp=3000, speed_sp=100)

try:
    while us.value()>45: #not ts.value():    # Stop program by pressing touch sensor button
        start = start + Ts
        while 0<(time.time()-start): # do nothing
            sleep(0.0001)
        print(str(start))
        red = cl.value(0)
        green=cl.value(1)
        blue=cl.value(2)
        
        #print("Red: " + str(red) + ", Green: " + str(green) + ", Blue: " + str(blue))
        [H, S, V] = rgb2hsv(red, green, blue)
        
        #mL.run_forever( speed_sp=0.4+V*speed)
        #mR.run_forever( speed_sp=(1.4-V)*speed)
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
            
#        elif last_white<1.1 or last_black<1.1:
#            course=0
#            
#            if last_black<last_white :
#                course=course-0.001
#            else:
#                course=course+0.001
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
