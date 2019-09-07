import RPi.GPIO as GPIO
import pyaudio
import  time
import struct
from scipy.fftpack import fft, fftfreq
import scipy
import random
import aubio
import numpy as num

#####Var#####
BUFFER_SIZE             = 2048 * 4
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE
p = pyaudio.PyAudio()

# Initiating Aubio's pitch detection object.
pDetection = aubio.pitch(METHOD, BUFFER_SIZE, HOP_SIZE, SAMPLE_RATE)
    # Set unit.
pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
pDetection.set_silence(-40)

#Pin numbers 
R = 17
G = 27
B = 22

#GPIO Var
freq= 100
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
pwmR = GPIO.PWM(R,freq)
pwmG = GPIO.PWM(G,freq)
pwmB = GPIO.PWM(B,freq)

    
def colorDisplay(red,green,blue, pitch):

    if pitch > 0:
        GPIO.setup(R, GPIO.OUT)
        GPIO.setup(G, GPIO.OUT)
        GPIO.setup(B, GPIO.OUT)
        
        pwmR.start(red)
        pwmG.start(blue)
        pwmB.start(green)
        
    if pitch == 0:
        GPIO.cleanup(R)
        GPIO.cleanup(G)
        GPIO.cleanup(B)


def audioMassager():
    while True:
        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
            dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        # Compute the energy (volume)
        # of the current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        volume = "{:6f}".format(volume)

        # Finally print the pitch and the volume.
        #print(str(pitch) + " " + str(volume))
        
        red = random.randint(0, 100)
        green = random.randint(0, 100)
        blue = random.randint(0, 100)
        
        colorDisplay(red ,green, blue, pitch)

        
#####Get Audio#####
mic = p.open(format=FORMAT, channels=CHANNELS,
        rate=SAMPLE_RATE, input=True,
        frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    
audioMassager()
