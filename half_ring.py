import random
import math

class Context:
    def __init__(self, maxWispSize, numPixels, wispTime, wispRate, emberHeight, shutterPin, timeStep, shutterTime):
        self.maxWispSize = maxWispSize
        self.numPixels = numPixels
        self.wispTime = wispTime
        self.wispRate = wispRate
        self.emberHeight = emberHeight
        self.shutterPin = shutterPin
        self.timeStep = timeStep
        self.shutterTime = shutterTime

class Pixels:
    def __init__(self, context):
        self.numPixels = context.numPixels
        self.pixels = [(0,0,0)] * context.numPixels

    def clear(self):
        self.pixels = [(0,0,0)] * self.numPixels

    def set(self, index, value):
        self.pixels[index] = value

class Wisp:
    def __init__(self, context):
        self.wispSpeed = context.numPixels / context.wispTime # pixels per second

    def reset(self, timeElapsed, size):
        self.size = size
        self.position = -self.size
        self.wispStart = timeElapsed

    def getPosition(self):
        return self.position

    def setPosition(self, timeElapsed):
        self.position = -self.size + math.floor((timeElapsed - self.wispStart) * self.wispSpeed)

class WispManager:
    def __init__(self, context):
        self.context = context
        self.wisps = []
        self.lastWispTime = 0
        self.wispPool = []

    @property
    def wispRate(self):
        return self.context.wispRate

    @property
    def maxWispSize(self):
        return self.context.maxWispSize

    def step(self, timeElapsed):
        keepWisps = []
        
        for wisp in self.wisps:
            wisp.setPosition(timeElapsed)
            wispMin = max(wisp.getPosition(), 0)
            if wispMin > self.context.numPixels:
                self.wispPool.append(wisp)
                continue
            keepWisps.append(wisp)

        self.wisps = keepWisps

        if timeElapsed - self.lastWispTime - random.uniform(-self.wispRate / 2, self.wispRate / 2) > self.wispRate:
            self.lastWispTime = timeElapsed
            wispSize = random.randint(1, self.maxWispSize)
            if len(self.wispPool) > 0:
                wisp = self.wispPool.pop()
            else:
                wisp = Wisp(self.context)
            wisp.reset(timeElapsed, wispSize)
            self.wisps.append(wisp)

    def apply(self, pixels):
        if self.context.numPixels != len(pixels.pixels):
            raise Exception("can't apply wisps to different sized pixels")

        for wisp in self.wisps:
            wispMin = max(wisp.getPosition(), 0)
            wispMax = min(wisp.getPosition() + wisp.size, self.context.numPixels)
            
            for i in range(wispMin, wispMax):
                pixels.set(i, (0, 255, 0))
        

class Embers:
    def __init__(self, context):
        self.context = context

        self.magnitude = 0

    @property
    def numPixels(self):
        return self.context.numPixels

    @property
    def emberHeight(self):
        return self.context.emberHeight

    def step(self, timeElapsed):
        self.magnitude = math.sin(2 * math.pi * timeElapsed) * math.sin(2 * math.pi * timeElapsed * 9.123)
        
    def apply(self, pixels):
        emberPixels = math.ceil(self.emberHeight * self.numPixels)
        for i in range(emberPixels):
            pixels.set(i, (0, 40 + 20 * self.magnitude, 0))
        for i in range(emberPixels, self.numPixels):
            glow = 10 + 5 * self.magnitude
            pixels.set(i, (0, (self.numPixels - i) * glow / self.numPixels, 0))

