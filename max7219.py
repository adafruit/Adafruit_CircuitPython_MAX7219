_NOOP = const(0)
_DIGIT0 = const(1)
_DIGIT1 = const(2)
_DIGIT2 = const(3)
_DIGIT3 = const(4)
_DIGIT4 = const(5)
_DIGIT5 = const(6)
_DIGIT6 = const(7)
_DIGIT7 = const(8)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)


class Matrix8x8:
    def __init__(self, spi, cs):
        """
        Driver for a single MAX7219-based LED matrix.

        >>> import max7219
        >>> from machine import Pin, SPI
        >>> spi = SPI(10000000, miso=Pin(12), mosi=Pin(13), sck=Pin(14))
        >>> display = max7219.Matrix8x8(spi, Pin(2))
        >>> display.fill(True)
        >>> display.pixel(4, 4, False)
        >>> display.show()

        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8)
        self.init()

    def _register(self, command, data):
        self.cs.low()
        self.spi.write(bytearray([command, data]))
        self.cs.high()

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._register(command, data)

    def brightness(self, value):
        if not 0<= value <= 15:
            raise ValueError("Brightness out of range")
        self._register(_INTENSITY, value)

    def fill(self, color):
        data = 0xff if color else 0x00
        for y in range(8):
            self.buffer[y] = data

    def pixel(self, x, y, color=None):
        if color is None:
            return bool(self.buffer[y] & 1 << x)
        elif color:
            self.buffer[y] |= 1 << x
        else:
            self.buffer[y] &= ~(1 << x)

    def show(self):
        for y in range(8):
            self._register(_DIGIT0 + y, self.buffer[y])

