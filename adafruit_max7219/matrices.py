# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Daniel Flanagan
#
# SPDX-License-Identifier: MIT

"""
`adafruit_max7219.matrices`
====================================================
"""
from micropython import const
from adafruit_framebuf import BitmapFont
from adafruit_max7219 import max7219

try:
    # Used only for typing
    from typing import Tuple
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

    :param ~busio.SPI spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    :param int width: the number of pixels wide
    :param int height: the number of pixels high
    :param int rotation: the number of times to rotate the coordinate system (default 1)
    """

    def __init__(
        self,
        spi: busio.SPI,
        cs: digitalio.DigitalInOut,
        width: int,
        height: int,
        *,
        rotation: int = 1
    ):
        super().__init__(width, height, spi, cs)

        self.y_offset = width // 8
        self.y_index = self._calculate_y_coordinate_offsets()

        self.framebuf.rotation = rotation
        self.framebuf.fill_rect = self._fill_rect
        self._font = None

    def _calculate_y_coordinate_offsets(self) -> None:
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

    def clear_all(self) -> None:
        """
        Clears all matrix leds.
        """
        self.fill(0)

    # pylint: disable=inconsistent-return-statements
    def pixel(self, xpos: int, ypos: int, bit_value: int = None) -> None:
        """
        Set one buffer bit

        :param int xpos: x position to set bit
        :param int ypos: y position to set bit
        :param int bit_value: value > 0 sets the buffer bit, else clears the buffer bit
        """
        if xpos < 0 or ypos < 0 or xpos >= self.width or ypos >= self.height:
            return
        buffer_x, buffer_y = self._pixel_coords_to_framebuf_coords(xpos, ypos)
        return super().pixel(buffer_x, buffer_y, bit_value=bit_value)

    def _pixel_coords_to_framebuf_coords(self, xpos: int, ypos: int) -> Tuple[int]:
        """
        Convert matrix pixel coordinates into coordinates in the framebuffer

        :param int xpos: x position
        :param int ypos: y position
        :return: framebuffer coordinates (x, y)
        :rtype: Tuple[int]
        """
        return (xpos - ((xpos // 8) * 8)) % 8, xpos // 8 + self.y_index[
            ypos * self.y_offset
        ]

    def _get_pixel(self, xpos: int, ypos: int) -> int:
        """
        Get value of a matrix pixel

        :param int xpos: x position
        :param int ypos: y position
        :return: value of pixel in matrix
        :rtype: int
        """
        x, y = self._pixel_coords_to_framebuf_coords(xpos, ypos)
        buffer_value = self._buffer[-1 * y - 1]
        return ((buffer_value & 2**x) >> x) & 1

    # Adafruit Circuit Python Framebuf Scroll Function
    # Authors: Kattni Rembor, Melissa LeBlanc-Williams and Tony DiCola, for Adafruit Industries
    # License: MIT License (https://opensource.org/licenses/MIT)
    def scroll(self, delta_x: int, delta_y: int) -> None:
        """
        Srcolls the display using delta_x, delta_y.

        :param int delta_x: positions to scroll in the x direction
        :param int delta_y: positions to scroll in the y direction
        """
        if delta_x < 0:
            shift_x = 0
            xend = self.width + delta_x
            dt_x = 1
        else:
            shift_x = self.width - 1
            xend = delta_x - 1
            dt_x = -1
        if delta_y < 0:
            y = 0
            yend = self.height + delta_y
            dt_y = 1
        else:
            y = self.height - 1
            yend = delta_y - 1
            dt_y = -1
        while y != yend:
            x = shift_x
            while x != xend:
                self.pixel(x, y, self._get_pixel(x - delta_x, y - delta_y))
                x += dt_x
            y += dt_y

    def rect(
        self, x: int, y: int, width: int, height: int, color: int, fill: bool = False
    ) -> None:
        """
        Draw a rectangle at the given position of the given size, color, and fill.

        :param int x: x position
        :param int y: y position
        :param int width: width of rectangle
        :param int height: height of rectangle
        :param int color: color of rectangle
        :param bool fill: 1 pixel outline or filled rectangle (default: False)
        """
        # pylint: disable=too-many-arguments
        for row in range(height):
            y_pos = row + y
            for col in range(width):
                x_pos = col + x
                if fill:
                    self.pixel(x_pos, y_pos, color)
                elif y_pos in (y, y + height - 1) or x_pos in (x, x + width - 1):
                    self.pixel(x_pos, y_pos, color)
                else:
                    continue

    def _fill_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """
        Draw a filled rectangle at the given position of the given size, color.

        :param int x: x position
        :param int y: y position
        :param int width: width of rectangle
        :param int height: height of rectangle
        :param int color: color of rectangle
        """
        # pylint: disable=too-many-arguments
        return self.rect(x, y, width, height, color, True)

    # Adafruit Circuit Python Framebuf Text Function
    # Authors: Kattni Rembor, Melissa LeBlanc-Williams and Tony DiCola, for Adafruit Industries
    # License: MIT License (https://opensource.org/licenses/MIT)
    def text(
        self,
        strg: str,
        xpos: int,
        ypos: int,
        color: int = 1,
        *,
        font_name: str = "font5x8.bin",
        size: int = 1
    ) -> None:
        """
        Draw text in the matrix.

        :param str strg: string to place in to display
        :param int xpos: x position of LED in matrix
        :param int ypos: y position of LED in matrix
        :param int color: > 1 sets the text, otherwise resets
        :param str font_name: path to binary font file (default: "font5x8.bin")
        :param int size: size of the font, acts as a multiplier
        """
        for chunk in strg.split("\n"):
            if not self._font or self._font.font_name != font_name:
                # load the font!
                self._font = BitmapFont(font_name)
            width = self._font.font_width
            height = self._font.font_height
            for i, char in enumerate(chunk):
                char_x = xpos + (i * (width + 1)) * size
                if (
                    char_x + (width * size) > 0
                    and char_x < self.width
                    and ypos + (height * size) > 0
                    and ypos < self.height
                ):
                    self._font.draw_char(
                        char, char_x, ypos, self.framebuf, color, size=size
                    )
            ypos += height * size
