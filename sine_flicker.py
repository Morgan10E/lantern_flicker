import math
import random
import board
import time
import neopixel

import fire
import shutter

SHUTTER_PIN = board.D3
SHUTTER_TIME = .1 # seconds

FIRE_PIXEL_PIN = board.D8
FIRE_BASELINE = 0.1 # % height of lantern
FIRE_AMPLITUDE = 0.4
FIRE_RATE = 10 # flickers per second
FIRE_VARIANCE = 0.15
FIRE_INTENSITY = 200
MASSIVE_REDUCER = 10

NUM_PIXELS = 72
PIXEL_RING = math.ceil(NUM_PIXELS / 2)
HALF_RING = math.ceil(PIXEL_RING / 2)
QUARTER_RING = math.ceil(HALF_RING / 2)

SLEEP_DUR = 0.01 # seconds

boardPixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

firePixels = neopixel.NeoPixel(FIRE_PIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False)

lanternFire = fire.Fire(FIRE_BASELINE, FIRE_AMPLITUDE, FIRE_RATE)
lanternShutter = shutter.Shutter(SHUTTER_PIN, SHUTTER_TIME, SLEEP_DUR)

def clearPixels():
    for i in range(NUM_PIXELS):
        firePixels[i] = (0,0,0)

def setAllPixels():
    for i in range(NUM_PIXELS):
        firePixels[i] = (255,255,255)

timeElapsed = 0

randR = random.randrange(255)
randG = random.randrange(255)
randB = random.randrange(255)
print(f"{randR}, {randG}, {randB}")


while True:
    boardPixel[0] = (randR, randG, randB)
    boardPixel.show()
    clearPixels()
    # setAllPixels()

    time.sleep(SLEEP_DUR)

    # standard flicker
    fireHeight = lanternFire.getStandardFireHeight(timeElapsed) * HALF_RING
    for i in range(4): # on each half ring
        randomness = FIRE_VARIANCE * random.uniform(-1,1)
        cornerHeight = fireHeight + randomness * HALF_RING
        for k in range(HALF_RING):
            pixelHeight = k if i % 2 == 0 else HALF_RING - k
            pixelValue = FIRE_INTENSITY
            if pixelHeight < cornerHeight:
                pixelValue = FIRE_INTENSITY + (255 - FIRE_INTENSITY) * (cornerHeight - pixelHeight) / cornerHeight
            else:
                pixelValue = (FIRE_INTENSITY - FIRE_INTENSITY * (pixelHeight - cornerHeight) / (HALF_RING - cornerHeight)) / MASSIVE_REDUCER
            firePixels[i * HALF_RING + k] = (0, pixelValue, 0)
    
    # for i in range(NUM_PIXELS):
    #     if i % PIXEL_RING < fireHeight or (NUM_PIXELS - i) % PIXEL_RING < fireHeight:
    #         firePixels[i] = (0, 255, 0)

    # apply shutter
    shutterPosition = lanternShutter.getShutterPosition()
    blackout = math.ceil(QUARTER_RING * shutterPosition)
    for i in range(blackout): # blackout pixels
        for k in range(4): # on each half ring
            firePixels[k * HALF_RING + i] = (0,0,0) # going forward
            firePixels[(k + 1) * HALF_RING - i - 1] = (0,0,0) # going backward

    firePixels.show()
    time.sleep(SLEEP_DUR)

    timeElapsed = timeElapsed + SLEEP_DUR