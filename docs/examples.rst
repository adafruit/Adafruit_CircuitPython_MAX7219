Examples
********

For software SPI::

max7219.Matrix8x8 Example
#########################

    import max7219
    from board import TX, RX, A2
    import busio

    clk = RX
    din = TX
    cs = A2
    spi = busio.SPI(clk, MOSI=din)
    display = max7219.Matrix8x8(spi, cs)
    display.fill(True)
    display.pixel(4, 4, False)
    display.show()

max7219.BDCDDigits Example
######################

    import max7219
    from board import TX, RX, A2
    import busio

    clk = RX
    din = TX
    cs = A2
    spi = busio.SPI(clk, MOSI=din)
    display = max7219.BCDDigits(spi, cs, nDigits=8)
    display.clearAll()
    display.setIntDigits(0,8,76543210)
    display.show()
