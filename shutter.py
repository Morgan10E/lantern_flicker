import digitalio

class Shutter:
    def __init__(self,shutterPin, shutterTime, timeStep):
        self.shutterButton = digitalio.DigitalInOut(shutterPin)
        self.shutterButton.direction = digitalio.Direction.INPUT
        self.shutterButton.pull = digitalio.Pull.UP

        self.deltaShutterPosition = timeStep / shutterTime
        self.shutterIsClosing = False # start with button not pressed
        self.shutterPosition = 0 # 0 is open, 1 is closed

    def getShutterPosition(self):
        if not self.shutterButton.value: # shutter is closing
            self.shutterPosition = self.shutterPosition + self.deltaShutterPosition if self.shutterPosition + self.deltaShutterPosition < 1 else 1
        else:
            self.shutterPosition = self.shutterPosition - self.deltaShutterPosition if self.shutterPosition - self.deltaShutterPosition > 0 else 0
        return self.shutterPosition