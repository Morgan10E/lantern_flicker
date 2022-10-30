
## Backstory
This was a project for a Halloween costume (many great projects are for Halloween costumes) where I needed a cool spooky lantern with green fire. Initially the plan was to do an LED grid and animate the fire - I had a whole proof-of-concept and everything - but mounting the LEDs in a grid bi-directionally in a metal lantern clearly not meant for it proved to be too challenging. So ring lighting was the next best thing.

## Overview
This project assumes the LEDs are arrayed in rings, with the LED string beginning and ending at the bottom. Each half strip is simulated independently to get a nice random flickering effect. There are three key portions of the simulation:
1. Embers
2. Wisps
3. Shutter

The embers and wisps are part of the fire simulation and are handled by the half ring. The embers are a constant flickering glow, while the wisps are patches of light that sweep up the lantern.
The shutter is an independent control triggered by a button that 'closes' the lantern.

## Components
- [Adafruit Kee Boar (KB2040)](https://www.adafruit.com/product/5302)
- [Adafruit Neopixel](https://www.adafruit.com/product/1138?length=2)

## Setup
1. Set up [CircuitPython](https://docs.circuitpython.org/en/latest/docs/index.html) on the Kee Boar. Adafruit has a great tutorial [here](https://learn.adafruit.com/adafruit-kb2040/circuitpython) for how to do so.
2. Build your circuit. I had something more complicated courtesy of a [friend with way higher standards than I have](https://github.com/CoolNamesAllTaken/), but once again [Adafruit has simple tutorials](https://learn.adafruit.com/adafruit-neopixel-uberguide?view=all#basic-connections).
