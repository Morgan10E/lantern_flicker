import math

class Fire:
    def __init__(self, fireBaseline, fireAmplitude, fireRate):
        self.fireBaseline = fireBaseline
        self.fireAmplitude = fireAmplitude
        self.fireRate = fireRate
        
    def getStandardFireHeight(self, timeElapsed):
        return self.fireBaseline + self.fireAmplitude * math.sin((2 * math.pi * timeElapsed * self.fireRate / 4) % (math.pi / 2)) # divide by 4 since a full 'flicker' is only the first quarter of a sine wave

