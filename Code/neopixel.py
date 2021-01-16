LED_CONTROL = 18

import board
import neopixel
from time import sleep





pixels = neopixel.NeoPixel(board.D18, 1)

pixels[0] = (255,0,0)

import detection
det = detection.Detection()
while(1):
    read = det.read_square(2,0)
    if read:
        pixels[0] = (255,0,0)
    else:
        pixels[0] = (0,0,255)
    sleep(0.2)
    
while(1):
    pixels[0] = (255,0,0)
    sleep(2)
    pixels[0] = (0,255,0)
    sleep(2)
    pixels[0] = (0,0,255)
    sleep(2)
    pixels[0] = (255,255,255)
    sleep(2)

