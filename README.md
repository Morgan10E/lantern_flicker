
## Backstory
This was a project for a Halloween costume (many great projects are for Halloween costumes) where I needed a cool spooky lantern with green fire. Initially the plan was to do an LED grid and animate the fire - I had a whole [proof-of-concept](https://github.com/Morgan10E/flicker_sim) and everything - but mounting the LEDs in a grid bi-directionally in a metal lantern clearly not meant for it proved to be too challenging. So ring lighting was the next best thing.

## Overview
This project assumes the LEDs are arrayed in rings, with the LED string beginning and ending at the bottom. Each half strip is simulated independently to get a nice random flickering effect. The half ring of pixels are managed by the Pixels class (which is currently basically just a wrapper on an array, with 0 being the pixel index at the bottom of the lantern and HALF_RING - 1 being the index of the pixel at the top). There are three key portions of the simulation that operate on our Pixels:
1. Embers - a constant flickering glow
2. Wisps - patches of light that sweep up the lantern
3. Shutter - an independent control triggered by a button that 'closes' the lantern

These are classes that simulate the current state of the ember, wisps, and shutter and then apply that state to our Pixels. We then do a final transformation from our Pixels to reverse half of the slices to be able to set the values to our Neopixels.

## Future Improvements
1. Make the simulation classes state-free functions
2. Have the Pixels class handle the transformation to Neopixel indices

## Components
- [Adafruit Kee Boar (KB2040)](https://www.adafruit.com/product/5302)
- [Adafruit Neopixel](https://www.adafruit.com/product/1138?length=2)

## Setup
1. Set up [CircuitPython](https://docs.circuitpython.org/en/latest/docs/index.html) on the Kee Boar. Adafruit has a great tutorial [here](https://learn.adafruit.com/adafruit-kb2040/circuitpython) for how to do so.
2. Build your circuit. I had something more complicated courtesy of a [friend with way higher standards than I have](https://github.com/CoolNamesAllTaken/), but once again [Adafruit has simple tutorials](https://learn.adafruit.com/adafruit-neopixel-uberguide?view=all#basic-connections).
