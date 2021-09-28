# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_max7219.bcddigits.BCDDigits`
====================================================
"""
from micropython import const
from adafruit_max7219 import max7219

try:
    # Used only for typing
    from typing import List
    import digitalio
    import busio
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MAX7219.git"

_DECODEMODE = const(9)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)


class BCDDigits(max7219.MAX7219):
    """
    Basic support for display on a 7-Segment BCD display controlled
    by a Max7219 chip using SPI.

    :param ~busio.SPI spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    :param int nDigits: number of led 7-segment digits; default 1; max 8
    """

    def __init__(self, spi: busio.SPI, cs: digitalio.DigitalInOut, nDigits: int = 1):
        self._ndigits = nDigits
        super().__init__(self._ndigits, 8, spi, cs)

    def init_display(self) -> None:

        for cmd, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, (2 ** self._ndigits) - 1),
            (_SHUTDOWN, 1),
        ):
            self.write_cmd(cmd, data)

        self.clear_all()
        self.show()

    def set_digit(self, dpos: int, value: int) -> None:
        """
        Display one digit.

        :param int dpos: the digit position; zero-based
        :param int value: integer ranging from 0->15
        """
        dpos = self._ndigits - dpos - 1
        for i in range(4):
            # print('digit {} pixel {} value {}'.format(dpos,i+4,v & 0x01))
            self.pixel(dpos, i, value & 0x01)
            value >>= 1

    def set_digits(self, start: int, values: List[int]) -> None:
        """
        Display digits from a list.

        :param int start: digit to start display zero-based
        :param list[int] values: list of integer values ranging from 0->15
        """
        for value in values:
            # print('set digit {} start {}'.format(d,start))
            self.set_digit(start, value)
            start += 1

    def show_dot(self, dpos: int, bit_value: int = None) -> None:
        """
        The decimal point for a digit.

        :param int dpos: the digit to set the decimal point zero-based
        :param int bit_value: value > zero lights the decimal point, else unlights the point
        """
        if 0 <= dpos < self._ndigits:
            # print('set dot {} = {}'.format((self._ndigits - d -1),col))
            self.pixel(self._ndigits - dpos - 1, 7, bit_value)

    def clear_all(self) -> None:
        """
        Clear all digits and decimal points.
        """
        self.fill(1)
        for i in range(self._ndigits):
            self.show_dot(i)

    def show_str(self, start: int, strg: str) -> None:
        """
        Displays a numeric str in the display.  Shows digits ``0-9``, ``-``, and ``.``.

        :param int start: start position to show the numeric string
        :param str strg: the numeric string
        """
        cpos = start
        for char in strg:
            # print('c {}'.format(c))
            value = 0x0F  # assume blank
            if "0" <= char <= "9":
                value = int(char)
            elif char == "-":
                value = 10  # minus sign
            elif char == ".":
                self.show_dot(cpos - 1, 1)
                continue
            self.set_digit(cpos, value)
            cpos += 1

    def show_help(self, start: int) -> None:
        """
        Display the word HELP in the display.

        :param int start: start position to show HELP
        """
        digits = [12, 11, 13, 14]
        self.set_digits(start, digits)
