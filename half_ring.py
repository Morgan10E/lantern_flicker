import random
import math

class Wisp:
    def __init__(self, size, timeElapsed, wispSpeed):
        self.size = size
        self.wispStart = timeElapsed
        self.wispSpeed = wispSpeed # pixels per second

    def getPosition(self, timeElapsed):
        return -self.size + math.floor((timeElapsed - self.wispStart) * self.wispSpeed)  


class FireFlicker:
    def __init__(self, numPixels, maxWispSize, emberHeight, wispSpeed, wispRate):
        self.pixels = [(0,0,0)] * numPixels
        self.maxWispSize = maxWispSize
        self.wisps = []
        self.lastWispTime = 0

        self.emberHeight = emberHeight
        self.wispSpeed = numPixels / wispSpeed
        self.wispRate = wispRate

    def clearPixels(self):
        for i in range(len(self.pixels)):
            self.pixels[i] = (0,0,0)

    def applyEmbers(self, timeElapsed):
        magnitude = math.sin(2 * math.pi * timeElapsed) * math.sin(2 * math.pi * timeElapsed * 9.123)
        emberPixels = math.ceil(self.emberHeight * len(self.pixels))
        for i in range(emberPixels):
            self.pixels[i] = (0, 40 + 20 * magnitude, 0)
        for i in range(emberPixels, len(self.pixels)):
            glow = 10 + 5 * magnitude
            self.pixels[i] = (0, (len(self.pixels) - i) * glow / len(self.pixels), 0)
        
    def addNewWisp(self, timeElapsed):
        if timeElapsed - self.lastWispTime - random.uniform(-self.wispRate / 2, self.wispRate / 2) > self.wispRate:
            self.lastWispTime = timeElapsed
            wispSize = random.randint(1, self.maxWispSize)
            self.wisps.append(Wisp(wispSize, timeElapsed, self.wispSpeed))

    def applyWisps(self, timeElapsed):
        keepWisps = []
        
        for wisp in self.wisps:
            wispMin = max(wisp.getPosition(timeElapsed), 0)
            if wispMin > len(self.pixels):
                continue
            wispMax = min(wisp.getPosition(timeElapsed) + wisp.size, len(self.pixels))
            for i in range(wispMin, wispMax):
                self.pixels[i] = (0, 255, 0)
            keepWisps.append(wisp)
        self.wisps = keepWisps
        
    def getFlicker(self, timeElapsed):
        self.clearPixels()
        self.applyEmbers(timeElapsed)
        self.addNewWisp(timeElapsed)
        self.applyWisps(timeElapsed)
        return self.pixels
