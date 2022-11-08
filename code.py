import math
import random
import board
import time
import neopixel

import shutter
import half_ring

SHUTTER_PIN = board.D3
SHUTTER_TIME = .1 # seconds

FIRE_PIXEL_PIN = board.D8

EMBER_HEIGHT = 0.1
WISP_TIME = 0.1 # seconds for wisp to travel to top
WISP_RATE = 1 # seconds between wisps
MAX_WISP_SIZE = 6

NUM_PIXELS = 72
NUM_RINGS = 2
PIXEL_RING = math.ceil(NUM_PIXELS / NUM_RINGS)
HALF_RING = math.ceil(PIXEL_RING / 2)
QUARTER_RING = math.ceil(HALF_RING / 2)

SLEEP_DUR = 0.01 # seconds

CONTEXT = half_ring.Context(MAX_WISP_SIZE, HALF_RING, WISP_TIME, WISP_RATE, EMBER_HEIGHT, SHUTTER_PIN, SLEEP_DUR, SHUTTER_TIME)

boardPixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

firePixels = neopixel.NeoPixel(FIRE_PIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False)

# lanternFire = fire.Fire(FIRE_BASELINE, FIRE_AMPLITUDE, FIRE_RATE)
lanternShutter = shutter.Shutter(CONTEXT)

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
embers = []
wispManager = []
for i in range(NUM_RINGS * 2):
    halfRings.append(half_ring.Pixels(CONTEXT))
    embers.append(half_ring.Embers(CONTEXT))
    wispManager.append(half_ring.WispManager(CONTEXT))

print("starting")

while True:
    boardPixel[0] = (randR, randG, randB)
    boardPixel.show()

    clearPixels()
    for i in range (NUM_RINGS * 2):
        halfRings[i].clear()

    for i in range (NUM_RINGS * 2):
        embers[i].step(timeElapsed)
        wispManager[i].step(timeElapsed)
    lanternShutter.step(timeElapsed)

    for i in range (NUM_RINGS * 2):
        embers[i].apply(halfRings[i])
        wispManager[i].apply(halfRings[i])
        lanternShutter.apply(halfRings[i])

    pixels = []
    for i in range(NUM_RINGS * 2):
        halfRingPixels = halfRings[i].pixels
        if i % 2 == 1:
            halfRingPixels.reverse()
        pixels = pixels + halfRingPixels

    for i in range(len(pixels)):
        firePixels[i] = pixels[i]

    firePixels.show()
    time.sleep(SLEEP_DUR)

    timeElapsed = timeElapsed + SLEEP_DUR