Examples
********

For software SPI on ESP8266::

    import max7219
    from machine import Pin, SPI
    spi = SPI(-1, 10000000, miso=Pin(12), mosi=Pin(13), sck=Pin(14))
    display = max7219.Matrix8x8(spi, Pin(2))
    display.fill(True)
    display.pixel(4, 4, False)
    display.show()

