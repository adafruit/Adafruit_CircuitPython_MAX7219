# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_max7219.matrices.Matrix8x8`
====================================================
"""
import time
from micropython import const
from adafruit_max7219 import max7219


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MAX7219.git"

_DECODEMODE = const(9)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)


class Matrix8x8(max7219.MAX7219):
    """
    Driver for a 8x8 LED matrix based on the MAX7219 chip.

    :param object spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    """

    def __init__(self, spi, cs, num=1):
        super().__init__(8, 8, spi, cs, num=num)

    def init_display(self):
        for cmd, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write([cmd, data] * self.num)

        self.fill(0)
        self.show()

    def text(self, strg, xpos, ypos, bit_value=1):
        """
        Draw text in the 8x8 matrix.

        :param int xpos: x position of LED in matrix
        :param int ypos: y position of LED in matrix
        :param string strg: string to place in to display
        :param bit_value: > 1 sets the text, otherwise resets
        """
        self.framebuf.text(strg, xpos, ypos, bit_value)

    def clear_all(self):
        """
        Clears all matrix leds.
        """
        self.fill(0)

    def display_str(self, data, delay=1):
        """
        Display string on led matrix by matrix length

        :param str: string that can be of any length.
        :param delay: transfer time from one screen to  another screen. default value is 1s

        """
        i = -1
        for char in data:
            i += 1
            self.fill(0)
            self.text(char, 1, 0)
            self.show_char_position(i % self.num)
            if i % self.num == self.num - 1:
                time.sleep(delay)
