Module classes
==============

Matrices
********

.. module:: adafruit_max7219.matrices

.. class:: Matrix8x8(spi, cs)

    Driver for a single MAX7219-based LED matrix.

    .. method:: brightness(value)

        Set the brightness.

    .. method:: fill(color)

        Fill the whole matrix with a specified color.

    .. method:: pixel(x, y, color=None)

        Set the color of a single pixel.

    .. method:: text(x, y, str)

        Position and set text on display; used for text scrolling
    
    .. method:: clear_all()

        sets all leds to off; same as fill(0)

    .. method:: show()

        Update the display.


BCDDigits
*********

.. module:: adafruit_max7219.bcddigits

.. class:: BCDDigits(spi, cs, nDigits=1)

    Driver for a single MAX7219-based LED matrix.


    .. method:: set_digit(d, v)
        
        set one digit in the display

    .. method:: show_dot(d, col=None)
        
        set the decimal point for a digit

    .. method:: show_str(s,str)
        
        displays a numeric str in the display.  shows digits 0-9, -, and .

    .. method:: show_help(s)
        
        display the word HELP in the display
        
    .. method:: brightness(value)

        Set the brightness.

    .. method:: pixel(x, y, color=None)

        Set the color of a single pixel.

    .. method:: clear_all()

        sets all leds to off

    .. method:: show()

        Update the display.
