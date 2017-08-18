Examples
********

For software SPI::

max7219.Matrix8x8 Example
#########################

.. code-block:: html

    from adafruit_max7219 import matrices
    from board import TX, RX, A2
    import busio

    clk = RX
    din = TX
    cs = A2
    spi = busio.SPI(clk, MOSI=din)
    display = matrices.Matrix8x8(spi, cs)
    display.fill(True)
    display.pixel(4, 4, False)
    display.show()

max7219.BCDDigits Example
######################

.. code-block:: html

    from adafruit_max7219 import bcddigits
    from board import TX, RX, A2
    import busio

    clk = RX
    din = TX
    cs = A2
    spi = busio.SPI(clk, MOSI=din)
    display = bcddigits.BCDDigits(spi, cs, nDigits=8)
    display.clearAll()
    display.showStr(0,8,'{:8.2f}'.format(-1234.561))
    display.show()
