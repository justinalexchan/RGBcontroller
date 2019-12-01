import RPi.GPIO as GPIO
import  time
import struct
import random
import numpy as num
import threading
import sys

#Pins
R = 17
G = 27
B = 22

#Random RGB rotation
def initalizePins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(R, GPIO.OUT)
    GPIO.setup(G, GPIO.OUT)
    GPIO.setup(B, GPIO.OUT)
    
def colorRotation(pin, freq, delay, clrChgSpd):
    global initialGPIO
    if initialGPIO == False:
        initalGPIO = True
        pwm = GPIO.PWM(pin,freq)
        pwm.start(0)
    
    global onOff 
    while onOff:
            for dutyCycle in range(0, 101, clrChgSpd):
                pwm.ChangeDutyCycle(dutyCycle)                
                time.sleep(delay)
            for dutyCycle in range(100, -1, -clrChgSpd):
                pwm.ChangeDutyCycle(dutyCycle)
                time.sleep(delay)
    GPIO.cleanup()
def inputThread():
    global onOff
    while True:
        userIn = raw_input('Command (on, off, exit): ')
        if userIn == 'off':
            print('Turning lights off...')
            onOff = False
        elif userIn == 'on':
            onOff = True
            print('Turning Lights on...')
            main()
        elif userIn == 'exit':
            onOff = False
            print('Exiting...')
            exit()
        
            
def colorChangeThread():
    threads = []
    threads.append(threading.Thread(target=colorRotation, args = (R, 300, 0.04, 5)))
    threads.append(threading.Thread(target=colorRotation, args = (G, 300, 0.07, 5)))
    threads.append(threading.Thread(target=colorRotation, args = (B, 300, 0.09, 5)))
    threads.append(threading.Thread(target=inputThread, args = ()))
        
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()

def main():
    initalizePins()
    colorChangeThread()

main()
GPIO.cleanup()
