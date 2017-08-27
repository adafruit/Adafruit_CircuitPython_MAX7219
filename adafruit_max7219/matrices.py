# The MIT License (MIT)
#
# Copyright (c) 2017 Dan Halbert
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
#

"""
:mod:`adafruit_max7219.matrices.Matrix8x8`
====================================================
"""
from adafruit_max7219 import max7219

_DECODEMODE = const(9)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix8x8(max7219.MAX7219):
    def __init__(self, spi, cs):
        """
        :param object spi: an spi busio or spi bitbangio object
        :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
        """
        super().__init__(8,8,spi,cs)

    def init_display(self):
        for cmd, data in (
                    (_SHUTDOWN, 0),
                    (_DISPLAYTEST, 0),
                    (_SCANLIMIT, 7),
                    (_DECODEMODE, 0),
                    (_SHUTDOWN, 1),
        ):
            self.write_cmd(cmd, data)

        self.fill(0)
        self.show()

    def text(self, str, x, y, col=1):
        """
        draw text in the 8x8 matrix.

        :param int x: x postiion of LED in matrix
        :param int y: y position of LED in matrix
        :param string str: string to place in to display
        """
        self.framebuf.text(str, x, y, col)

    def clear_all(self):
        """
        unlights all matrix leds
        """
        self.fill(0)
