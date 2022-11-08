import digitalio
import math

class Shutter:
    def __init__(self, context):
        self.shutterButton = digitalio.DigitalInOut(context.shutterPin)
        self.shutterButton.direction = digitalio.Direction.INPUT
        self.shutterButton.pull = digitalio.Pull.UP

        self.deltaShutterPosition = context.timeStep / context.shutterTime
        self.shutterIsClosing = False # start with button not pressed
        self.shutterPosition = 0 # 0 is open, 1 is closed

    def step(self, timeElapsed):
        if not self.shutterButton.value: # shutter is closing
            self.shutterPosition = self.shutterPosition + self.deltaShutterPosition if self.shutterPosition + self.deltaShutterPosition < 1 else 1
        else:
            self.shutterPosition = self.shutterPosition - self.deltaShutterPosition if self.shutterPosition - self.deltaShutterPosition > 0 else 0

    def apply(self, pixels):
        blackout = math.ceil(len(pixels.pixels) * self.shutterPosition)
        for i in range(blackout):
            pixels.set(i, (0,0,0))