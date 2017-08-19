# The MIT License (MIT)
#
# Copyright (c) 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_max7219.MAX7219` - MAX7219 LED Matrix/Digit Display Driver
========================================================================
CircuitPython library to support MAX7219 LED Matrix/Digit Display Driver.
This library supports the use of the MAX7219-based display in CircuitPython, 
either an 8x8 matrix or a 8 digit 7-segment numeric display.

see also
========
* matrices.Maxtrix8x8 is a class support an 8x8 led matrix display
* bcddigits.BCDDigits is a class that support the 8 digit 7-segment display

Beware that most CircuitPython compatible hardware are 3.3v logic level! Make
sure that the input pin is 5v tolerant.
* Author(s): Michael McWethy

Implementation Notes
--------------------
**Hardware:**
* Adafruit `MAX7219CNG LED Matrix/Digit Display Driver - MAX7219 <https://www.adafruit.com/product/453>`_ (Product ID: 453)
**Software and Dependencies:**
* Adafruit CircuitPython firmware (1.0.0+) for the ESP8622 and M0-based boards: https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
**Notes:**
#.  Datasheet: https://cdn-shop.adafruit.com/datasheets/MAX7219.pdf
"""
# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
import framebuf
import digitalio

from adafruit_bus_device import spi_device

# register definitions
_DIGIT0 = const(1)
_INTENSITY = const(10)


class MAX7219:
    
    def __init__(self, w, h, spi, cs,
                 baudrate=8000000, polarity=0, phase=0):
        """
        :param int w: the number of pixels wide
        :param int h: the number of pixels high
        :param object spi: an spi busio or spi bitbangio object
        :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal 
        """
        
        self.cs = cs
        self.cs.direction = digitalio.Direction.OUTPUT
        
        self.spiDevice = spi_device.SPIDevice(spi, cs, baudrate=baudrate,
                                               polarity=polarity, phase=phase)
       
        self.buffer = bytearray((h // 8) * w)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, w, h)

        self.w = w
        self.h = h

        self.init_display()

    def brightness(self, value):
        """
        control the brightness of the display
        :param int value: 0->15 dimmest to brightest
        """
        if not 0<= value <= 15:
            raise ValueError("Brightness out of range")
        self.write_cmd(_INTENSITY, value)

    def show(self):
        """
        update the display with recent changes in buffer 
        """
        for y in range(8):
            self.write_cmd(_DIGIT0 + y, self.buffer[y])

    def fill(self, col):
        """
        set all buffer bits to a col
        :param int col: value > 0 set the buffer bit, else clears the buffer bit
        """
        self.framebuf.fill(col)

    def pixel(self, x, y, col=None):
        """
        set one buffer bit
        :param int col: value > 0 set the buffer bit, else clears the buffer bit
        """
        col = 0x01 if col else 0x00
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)
    
    def write_cmd(self, cmd, data):
        #print('cmd {} data {}'.format(cmd,data))
        self.cs.value = False
        with self.spiDevice as spiDevice:        
            spiDevice.write(bytearray([cmd, data]))
