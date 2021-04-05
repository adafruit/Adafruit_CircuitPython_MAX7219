# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import random
from board import TX, RX, A2
import busio
import digitalio
from adafruit_max7219 import matrices

clk = RX
din = TX
cs = digitalio.DigitalInOut(A2)      
        
spi = busio.SPI(clk, MOSI=din)
display = matrices.Matrix8x8(spi, cs)

while True:
    display.brightness(1)

    display.fill(1)
    display.pixel(3, 3)
    display.pixel(3, 4)
    display.pixel(4, 3)
    display.pixel(4, 4)
    display.show()
    time.sleep(3.0)

    display.clear_all()
    s = 'Hello, World!'
    display.text(s[random.randint(0,len(s)-1)],0,0)

    # show random char in string s on the the first of cascaded matrixs.
    display.show(1) 
    for c in range(len(s)*8):
        display.fill(0)
        display.text(s,-c,0)
        
        # show scrolled string on the second of cascaded matrixs.
        display.show(2) 
        time.sleep(0.25)
