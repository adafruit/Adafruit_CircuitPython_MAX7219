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
:mod:`adafruit_max7219.bcddigits.BCDDigits`
====================================================
"""
from adafruit_max7219 import max7219

_DECODEMODE = const(9)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class BCDDigits(max7219.MAX7219):
    """
    Basic support for display on a 7-Segment BCD display controlled
    by a Max7219 chip using SPI.
    """
    def __init__(self, spi, cs, nDigits=1):
        """
        :param object spi: an spi busio or spi bitbangio object
        :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
        :param int nDigits: number of led 7-segment digits; default 1; max 8
        """
        self.nD = nDigits
        super().__init__(self.nD, 8 ,spi ,cs)

    def init_display(self):
        
        for cmd, data in (
                    (_SHUTDOWN, 0),
                    (_DISPLAYTEST, 0),
                    (_SCANLIMIT, 7),
                    (_DECODEMODE, (2**self.nD)-1),
                    (_SHUTDOWN, 1),
        ):
            self.write_cmd(cmd, data)        

        self.clear_all()
        self.show()

    def set_digit(self, d, v):
        """
        set one digit in the display
        :param int d: the digit position; zero-based 
        :param int v: integer ranging from 0->15
        """
        d = self.nD - d - 1
        for i in range(4):
            #print('digit {} pixel {} value {}'.format(d,i+4,v & 0x01))
            self.pixel(d,i,v & 0x01)
            v >>= 1
    
    def set_digits(self, s, ds):
        """
        set the display from a list
        :param int s: digit to start display zero-based
        :param list ds: list of integer values ranging from 0->15
        """
        for d in ds:
            #print('set digit {} start {}'.format(d,start))
            self.set_digit(s,d)
            s += 1

    def show_dot(self,d, col=None):
        """
        set the decimal point for a digit
        :param int d: the digit to set the decimal point zero-based 
        :param int col: value > zero lights the decimal point, else unlights the point
        """
        if d < self.nD and d >= 0:
            #print('set dot {} = {}'.format((self.nD - d -1),col))
            self.pixel(self.nD-d-1, 7,col)

    def clear_all(self):
        """
        clear all digits and decimal points
        """
        self.fill(1)
        for i in range(self.nD):
            self.show_dot(i)

    def show_str(self,s,str):        
        """
        displays a numeric str in the display.  shows digits 0-9, -, and .
        :param int s: start position to show the numeric string
        :param string str: the numeric string
        """
        ci = s
        for i in range (len(str)):
            c = str[i]
            # print('c {}'.format(c))
            v = 0x0f # assume blank 
            if c >= '0' and c<='9':
                v = int(c)
            elif c == '-':
                v = 10 # minus sign
            elif c == '.':
                self.show_dot(ci-1,1)
                continue
            self.set_digit(ci,v)
            ci += 1
    
    def show_help(self, s):
        """
        display the word HELP in the display
        :param int s: start position to show HELP
        """
        digits = [12,11,13,14]
        self.set_digits(s,digits)

