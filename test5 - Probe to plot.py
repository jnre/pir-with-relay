#!/usr/bin/python

import spidev
import time
import os
import math
from datetime import datetime
ref_volt = 3.311

spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel) << 4,0])
    data = ((adc[1]&3)<<8) +adc[2]
    return data

def ConvertVolts(data,places):
    volts = (data*ref_volt)/float(1023)
    volts = round(volts,places)
    return volts

channel0 = 0
channel1 = 1
count = 0
sleepdelay = 1
v = [0]
f = open('ProbeToPlot3.csv', 'w')
alpha = 0.0861302
y = [0]
    
    
NUMBER_OF_SAMPLES = 512

start_time = datetime.now()
    
for n in range (1, NUMBER_OF_SAMPLES):

    
    i = ReadChannel(channel0)
    j = ReadChannel(channel1)
    i = i - j
    v.append(ConvertVolts(i, 9))
        
    #stoptime = datetime.now()
    

stoptime = datetime.now()

for n in range (1, NUMBER_OF_SAMPLES):

    y.append(alpha*v[n]+(1-alpha)*y[n-1])


f.write("{},".format(y))

        

print("Probe time : {} milliseconds ".format((stoptime -start_time).microseconds/1000))
     
f.close()







