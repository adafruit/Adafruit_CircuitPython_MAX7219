Matrices
********

.. module:: max7219

.. class:: Matrix8x8(spi, cs)

    Driver for a single MAX7219-based LED matrix.

    .. method:: brightness(value)

        Set the brightness.

    .. method:: fill(color)

        Fill the whole matrix with a specified color.

    .. method:: pixel(x, y, color=None)

        Get or set the color of a single pixel.

    .. method:: show()

        Update the display.
