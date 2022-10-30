import random
import math

class Wisp:
    def __init__(self, position, size):
        self.position = position
        self.size = size

class FireFlicker:
    def __init__(self, numPixels, maxWispSize, emberHeight, wispSpeed, wispRate):
        self.pixels = [(0,0,0)] * numPixels
        self.maxWispSize = maxWispSize
        self.wisp = Wisp(0,0)
        self.wispStart = 0

        self.emberHeight = emberHeight
        self.wispSpeed = wispSpeed
        self.wispRate = wispRate

    def clearPixels(self):
        for i in range(len(self.pixels)):
            self.pixels[i] = (0,0,0)

    def applyEmbers(self, timeElapsed):
        magnitude = math.sin(2 * math.pi * timeElapsed) * math.sin(2 * math.pi * timeElapsed * 9)
        emberPixels = math.ceil(self.emberHeight * len(self.pixels))
        for i in range(emberPixels):
            self.pixels[i] = (0, 40 + 20 * magnitude, 0)
        for i in range(emberPixels, len(self.pixels)):
            glow = 10 + 5 * magnitude
            self.pixels[i] = (0, (len(self.pixels) - i) * glow / len(self.pixels), 0)
        

    def applyWisp(self, timeElapsed):
        if timeElapsed - self.wispStart - random.uniform(-self.wispRate / 2, self.wispRate / 2) > self.wispRate:
            self.wispStart = timeElapsed
            wispSize = random.randint(1, self.maxWispSize)
            self.wisp = Wisp(-wispSize, wispSize)
        else:
            self.wisp.position = math.floor((timeElapsed - self.wispStart) / self.wispSpeed * len(self.pixels))
            wispMin = self.wisp.position if self.wisp.position > 0 else 0
            wispMax = self.wisp.position + self.wisp.size if self.wisp.position + self.wisp.size < len(self.pixels) else len(self.pixels)
            for i in range(wispMin, wispMax):
                self.pixels[i] = (0, 255, 0)
        
    def getFlicker(self, timeElapsed):
        self.clearPixels()
        self.applyEmbers(timeElapsed)
        self.applyWisp(timeElapsed)
        return self.pixels