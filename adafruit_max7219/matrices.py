# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_max7219.matrices.Matrix8x8`
====================================================
"""
from micropython import const
from adafruit_max7219 import max7219

try:
    # Used only for typing
    import typing  # pylint: disable=unused-import
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


class Matrix8x8(max7219.MAX7219):
    """
    Driver for a 8x8 LED matrix based on the MAX7219 chip.

    :param ~busio.SPI spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    """

    def __init__(self, spi: busio.SPI, cs: digitalio.DigitalInOut):
        super().__init__(8, 8, spi, cs)

    def init_display(self) -> None:
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

    def text(self, strg: str, xpos: int, ypos: int, bit_value: int = 1) -> None:
        """
        Draw text in the 8x8 matrix.

        :param str strg: string to place in to display
        :param int xpos: x position of LED in matrix
        :param int ypos: y position of LED in matrix
        :param int bit_value: > 1 sets the text, otherwise resets
        """
        self.framebuf.text(strg, xpos, ypos, bit_value)

    def clear_all(self) -> None:
        """
        Clears all matrix leds.
        """
        self.fill(0)


class CustomMatrix(max7219.ChainableMAX7219):
    """
    Driver for a custom 8x8 LED matrix constellation based on daisy chained MAX7219 chips.

    :param object spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    :param int width: the number of pixels wide
    :param int height: the number of pixels high
    :param int rotation: the number of times to rotate the coordinate system (default 1)
    """

    def __init__(self, spi, cs, width, height, *, rotation=1):
        super().__init__(width, height, spi, cs)

        self.y_offset = width // 8
        self.y_index = self._calculate_y_coordinate_offsets()

        self.framebuf.rotation = rotation

    def _calculate_y_coordinate_offsets(self):
        y_chunks = []
        for _ in range(self.chain_length // (self.width // 8)):
            y_chunks.append([])
        chunk = 0
        chunk_size = 0
        for index in range(self.chain_length * 8):
            y_chunks[chunk].append(index)
            chunk_size += 1
            if chunk_size >= (self.width // 8):
                chunk_size = 0
                chunk += 1
                if chunk >= len(y_chunks):
                    chunk = 0

        y_index = []
        for chunk in y_chunks:
            y_index += chunk
        return y_index

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

    def pixel(self, xpos, ypos, bit_value=None):
        """
        Set one buffer bit

        :param xpos: x position to set bit
        :param ypos: y position to set bit
        :param int bit_value: value > 0 sets the buffer bit, else clears the buffer bit
        """

        buffer_y = xpos // 8 + self.y_index[ypos * self.y_offset]
        buffer_x = (xpos - ((xpos // 8) * 8)) % 8
        return super().pixel(buffer_x, buffer_y, bit_value=bit_value)
