# SPDX-FileCopyrightText: 2016 Philip R. Moyer  for Adafruit Industries
# SPDX-FileCopyrightText: 2016 Radomir Dopieralski for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_max7219.max7219` - MAX7219 LED Matrix/Digit Display Driver
========================================================================
CircuitPython library to support MAX7219 LED Matrix/Digit Display Driver.
This library supports the use of the MAX7219-based display in CircuitPython,
either an 8x8 matrix or a 8 digit 7-segment numeric display.

See Also
=========
* matrices.Maxtrix8x8 is a class support an 8x8 led matrix display
* bcddigits.BCDDigits is a class that support the 8 digit 7-segment display

Beware that most CircuitPython compatible hardware are 3.3v logic level! Make
sure that the input pin is 5v tolerant.

* Author(s): Michael McWethy

Implementation Notes
--------------------
**Hardware:**

* Adafruit `MAX7219CNG LED Matrix/Digit Display Driver -
  MAX7219 <https://www.adafruit.com/product/453>`_ (Product ID: 453)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

**Notes:**
#.  Datasheet: https://cdn-shop.adafruit.com/datasheets/MAX7219.pdf
"""
# MicroPython MAX7219 driver, SPI interfaces
import digitalio
from adafruit_bus_device import spi_device
from micropython import const
import adafruit_framebuf as framebuf

try:
    # Used only for typing
    import busio
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MAX7219.git"

# register definitions
_DIGIT0 = const(1)
_INTENSITY = const(10)


class MAX7219:
    """
    MAX2719 - driver for displays based on max719 chip_select

    :param int width: the number of pixels wide
    :param int height: the number of pixels high
    :param ~busio.SPI spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut chip_select: digital in/out to use as chip select signal
    :param int baudrate: for SPIDevice baudrate (default 8000000)
    :param int polarity: for SPIDevice polarity (default 0)
    :param int phase: for SPIDevice phase (default 0)
    """

    def __init__(
        self,
        width: int,
        height: int,
        spi: busio.SPI,
        cs: digitalio.DigitalInOut,
        *,
        baudrate: int = 8000000,
        polarity: int = 0,
        phase: int = 0
    ):

        self._chip_select = cs
        self._chip_select.direction = digitalio.Direction.OUTPUT

        self._spi_device = spi_device.SPIDevice(
            spi, cs, baudrate=baudrate, polarity=polarity, phase=phase
        )

        self._buffer = bytearray((height // 8) * width)
        self.framebuf = framebuf.FrameBuffer1(self._buffer, width, height)

        self.width = width
        self.height = height

        self.init_display()

    def init_display(self) -> None:
        """Must be implemented by derived class (``matrices``, ``bcddigits``)"""

    def brightness(self, value: int) -> None:
        """
        Controls the brightness of the display.

        :param int value: 0->15 dimmest to brightest
        """
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self.write_cmd(_INTENSITY, value)

    def show(self) -> None:
        """
        Updates the display.
        """
        for ypos in range(8):
            self.write_cmd(_DIGIT0 + ypos, self._buffer[ypos])

    def fill(self, bit_value: int) -> None:
        """
        Fill the display buffer.

        :param int bit_value: value > 0 set the buffer bit, else clears the buffer bit
        """
        self.framebuf.fill(bit_value)

    def pixel(self, xpos: int, ypos: int, bit_value: int = None) -> None:
        """
        Set one buffer bit

        :param int xpos: x position to set bit
        :param int ypos: y position to set bit
        :param int bit_value: value > 0 sets the buffer bit, else clears the buffer bit
        """
        bit_value = 0x01 if bit_value else 0x00
        self.framebuf.pixel(xpos, ypos, bit_value)

    def scroll(self, delta_x: int, delta_y: int) -> None:
        """
        Srcolls the display using delta_x,delta_y.

        :param int delta_x: positions to scroll in the x direction
        :param int delta_y: positions to scroll in the y direction
        """
        self.framebuf.scroll(delta_x, delta_y)

    def write_cmd(self, cmd, data) -> None:
        # pylint: disable=no-member
        """Writes a command to spi device."""
        # print('cmd {} data {}'.format(cmd,data))
        self._chip_select.value = False
        with self._spi_device as my_spi_device:
            my_spi_device.write(bytearray([cmd, data]))
