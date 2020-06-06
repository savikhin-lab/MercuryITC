print "Start: Mercury ITC script"
import visa                         #import NI-VISA wrapper (interface with equipment). Function calls are visa.function()
import sys                          #import system lib (system == python interpreter, not the os)
import numpy                        #import numeric library
import time                         #import time library
import os                           #import operating system library
import matplotlib.pyplot as plt
import serial, sys, time, glob, struct
import h5py

def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False

def TempInitialize():
    rm = visa.ResourceManager()
    reslist=rm.list_resources()
    print 'List of Resources \n' ,reslist
    mercury = rm.open_resource('ASRL10::INSTR')
    print(mercury.query("*IDN?"))
    return mercury
def TempGet():
    flag = True
    while flag:
        temperature = mercury.query("READ:DEV:MB1.T1:TEMP:SIG:TEMP\n")
        print 'attempt=',temperature[30:37]
        if isfloat(temperature[30:37]):
            #print 'Temperature is:',temperature[30:37]
            T_signal = float(temperature[30:37])
            flag = False
    return T_signal
print '----------------------------------------'
mercury = TempInitialize()
mercury.read_termination = '\n'
mercury.write_termination = '\n'
print(mercury.query("READ:SYS:CAT?"))
TempArray = numpy.zeros((1,2)) 
A = numpy.zeros((1,2)) 
plt.figure(1)
plt.ion()
TempArray[0,1] = TempGet()
TempArray[0,0] = int(time.time())

while True:
    print 'Temperature is:', TempGet()
    A[0,1] = TempGet()
    A[0,0] = int(time.time())
    TempArray = numpy.vstack((A,TempArray))
    print TempArray
    plt.clf()
    plt.plot(TempArray[:,0],TempArray[:,1])
    numpy.savetxt('temperature_6-26-6-27.txt', TempArray, delimiter=',') 
    plt.pause(10)
    
 

