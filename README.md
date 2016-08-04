#!/usr/bin/python

import spidev
import time
import os
import math
from datetime import datetime 

channel = 0
ref_volt = 3.311

#operationMode = 0    # differential
operationMode = 8    # single channel

adcRes = (1 << 10) - 1


spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
    adc = spi.xfer([1,(operationMode + channel) << 4,0])
    data = ((adc[1]&3)<<8) +adc[2]
    return data

def ConvertVolts(data,places):
    volts = (data*ref_volt)/float(adcRes)
    volts = round(volts,places)
    return volts

pot_channel = 0

delay = 2

def GetMaxMinSampleVoltage(channel):
    NUMBER_OF_SAMPLES = 1000
    SUPPLYVOLTAGE = ref_volt
    Loops = 2000   # SCT013
    Rb = 33        # Ohm

    #sumI = 0
    sumV = 0

    sampleI = 512
    filteredI = 0

    maxValue = -ref_volt
    minValue = ref_volt

    for n in range (0, NUMBER_OF_SAMPLES):
       
        lastSampleI = sampleI
        sampleI = ReadChannel(channel)

        lastFilteredI = filteredI
        filteredI = 0.996*(lastFilteredI+sampleI-lastSampleI)

        #sqI = filteredI * filteredI
        #sumI += sqI

        voltage = ConvertVolts(filteredI, 9)
        sqV = voltage * voltage
        sumV += sqV

        # calculate max, min voltage
        if maxValue < voltage:
            maxValue = voltage

        if minValue > voltage:
            minValue = voltage

    #Irms = I_RATIO * math.sqrt(sumI / NUMBER_OF_SAMPLES)
    #return (minValue, maxValue, Irms)

    Vrms =  math.sqrt(sumV / NUMBER_OF_SAMPLES)
    Irms =  Loops * Vrms / Rb

    return (minValue, maxValue, Vrms, Irms)


while True:
    start_time = datetime.now()
    values = GetMaxMinSampleVoltage(channel)
    stoptime = datetime.now()

    print("T: {}ms, Irms: {}A, Vrms: {}V, Vmin: {}V, Vmax: {}V".format((stoptime-start_time).microseconds/1000, values[3], values[2], values[0], values[1]))

    time.sleep(delay)

