
Module classes
==============

Matrices
********

.. module:: adafruit_max7219.matrices

.. class:: Matrix8x8(spi, cs)

    Driver for a single MAX7219-based 8x8 LED matrix.

    :param object spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal

    .. method:: brightness(value)

        control the brightness of the display

        :param int value: 0->15 dimmest to brightest

    .. method:: fill(color)

        Fill the whole matrix with a specified color.

        :param int color: None or False or 0 turn LED off, anything else turns LED on

    .. method:: pixel(x, y, color=None)

        Set the color of a single pixel.

        :param int x: x postiion of LED in matrix
        :param int y: y position of LED in matrix
        :param int color: value > zero lights the decimal point, else unlights the point

    .. method:: text(x, y, str)

        Position and set text on display; used for text scrolling

        :param int x: x postiion of LED in matrix
        :param int y: y position of LED in matrix
        :param string str: string to place in to display

    .. method:: clear_all()

        sets all leds to off; same as fill(0)

    .. method:: show()

        Update the display.


BCDDigits
*********

.. module:: adafruit_max7219.bcddigits

.. class:: BCDDigits(spi, cs, nDigits=1)

    Driver for one to 8 MAX7219-based 7-Segment LED display.

    :param object spi: an spi busio or spi bitbangio object
    :param ~digitalio.DigitalInOut cs: digital in/out to use as chip select signal
    :param int nDigits: number of led 7-segment digits; default 1; max 8

    .. method:: set_digit(d, v)

        set one digit in the display

        :param int d: the digit position; zero-based
        :param int v: integer ranging from 0->15

    .. method:: show_dot(d, col=None)

        set the decimal point for a digit

        :param int d: the digit to set the decimal point zero-based
        :param int col: value > zero lights the decimal point, else unlights the point

    .. method:: show_str(s,str)

        displays a numeric str in the display.  shows digits 0-9, -, and .

        :param int s: start position to show the numeric string
        :param string str: the numeric string

    .. method:: show_help(s)

        display the word HELP in the display

        :param int s: start position to show HELP

    .. method:: brightness(value)

       control the brightness of the display

       :param int value: 0->15 dimmest to brightest

    .. method:: clear_all()

        sets all leds to off

    .. method:: show()

        Update the display.
