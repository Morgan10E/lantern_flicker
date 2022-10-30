import math
import random
import board
import time
import neopixel

import fire
import shutter
import half_ring

SHUTTER_PIN = board.D3
SHUTTER_TIME = .1 # seconds

FIRE_PIXEL_PIN = board.D8
# FIRE_BASELINE = 0.1 # % height of lantern
# FIRE_AMPLITUDE = 0.4
# FIRE_RATE = 10 # flickers per second
# FIRE_VARIANCE = 0.15
# FIRE_INTENSITY = 200
# MASSIVE_REDUCER = 10

EMBER_HEIGHT = 0.1
WISP_SPEED = 0.1 # seconds for wisp to travel to top
WISP_RATE = 3 # seconds between wisps

NUM_PIXELS = 72
NUM_RINGS = 2
PIXEL_RING = math.ceil(NUM_PIXELS / NUM_RINGS)
HALF_RING = math.ceil(PIXEL_RING / 2)
QUARTER_RING = math.ceil(HALF_RING / 2)

SLEEP_DUR = 0.01 # seconds

boardPixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

firePixels = neopixel.NeoPixel(FIRE_PIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False)

# lanternFire = fire.Fire(FIRE_BASELINE, FIRE_AMPLITUDE, FIRE_RATE)
lanternShutter = shutter.Shutter(SHUTTER_PIN, SHUTTER_TIME, SLEEP_DUR)

def clearPixels():
    for i in range(NUM_PIXELS):
        firePixels[i] = (0,0,0)

def setAllPixels():
    for i in range(NUM_PIXELS):
        firePixels[i] = (255,255,255)

timeElapsed = 0 # TODO use time from the board

randR = random.randrange(255)
randG = random.randrange(255)
randB = random.randrange(255)
print(f"{randR}, {randG}, {randB}")

halfRings = []
for i in range(NUM_RINGS * 2):
    halfRings.append(half_ring.FireFlicker(HALF_RING, 6, EMBER_HEIGHT, WISP_SPEED, WISP_RATE))
print("starting")

while True:
    boardPixel[0] = (randR, randG, randB)
    boardPixel.show()
    clearPixels()
    # setAllPixels()

    pixels = []
    for i in range(NUM_RINGS * 2):
        halfRingPixels = halfRings[i].getFlicker(timeElapsed)
        if i % 2 == 1:
            halfRingPixels.reverse()
        pixels = pixels + halfRingPixels
    
    for i in range(len(pixels)):
        firePixels[i] = pixels[i]
    
    
    # for i in range(NUM_PIXELS):
    #     if i % PIXEL_RING < fireHeight or (NUM_PIXELS - i) % PIXEL_RING < fireHeight:
    #         firePixels[i] = (0, 255, 0)

    # apply shutter
    shutterPosition = lanternShutter.getShutterPosition()
    blackout = math.ceil(QUARTER_RING * shutterPosition)
    for i in range(blackout): # blackout pixels
        for k in range(NUM_RINGS * 2): # on each half ring
            firePixels[k * HALF_RING + i] = (0,0,0) # going forward
            firePixels[(k + 1) * HALF_RING - i - 1] = (0,0,0) # going backward

    firePixels.show()
    time.sleep(SLEEP_DUR)

    timeElapsed = timeElapsed + SLEEP_DUR