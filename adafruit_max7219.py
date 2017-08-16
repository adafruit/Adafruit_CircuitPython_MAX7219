# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
import time
import framebuf
import digitalio

from adafruit_bus_device import spi_device


# register definitions
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


class MAX7219_SPI:

    def __init__(self, width, height, spi, csPin,
                 baudrate=8000000, polarity=0, phase=0):
        
        cs = digitalio.DigitalInOut(csPin)
        self.cs = cs
        self.cs.direction = digitalio.Direction.OUTPUT
        
        self.spiDevice = spi_device.SPIDevice(spi, cs, baudrate=baudrate,
                                               polarity=polarity, phase=phase)

        
        self.buffer = bytearray((height // 8) * width)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, width, height)

        self.width = width
        self.height = height

        self.init_display()

    def brightness(self, value):
        """
        control the brightness of the display
        param: value - 0->15 dimmest to brightest
        """
        if not 0<= value <= 15:
            raise ValueError("Brightness out of range")
        self.write_cmd(_INTENSITY, value)

    def show(self):
        """
        update the display with recent changes in buffer
        """
        for y in range(8):
            self.write_cmd(_DIGIT0 + y, self.buffer[y])

    def fill(self, col):
        """
        set all buffer bits to a col
        param: col - value > 0 set the buffer bit, else clears the buffer bit
        """
        self.framebuf.fill(col)

    def pixel(self, x, y, col=None):
        """
        set one buffer bit
        param: col - value > 0 set the buffer bit, else clears the buffer bit
        """
        col = 0x01 if col else 0x00
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)
    
    def write_cmd(self, command, data):
        print('command {} data {}'.format(command,data))
        self.cs.value = False
        with self.spiDevice as spiDevice:        
            spiDevice.write(bytearray([command, data]))


class Matrix8x8(MAX7219_SPI):
    def __init__(self, spi, csPin):
        super().__init__(8,8,spi,csPin)

    def init_display(self):
        for command, data in (
                    (_SHUTDOWN, 0),
                    (_DISPLAYTEST, 0),
                    (_SCANLIMIT, 7),
                    (_DECODEMODE, 0),
                    (_SHUTDOWN, 1),
        ):
            self.write_cmd(command, data)        

        self.fill(0)
        self.show()

    def text(self, string, x, y, col=1):
        """
        draw text in the 8x8 matrix.
        """
        self.framebuf.text(string, x, y, col)

    def clearAll():
        """
        unlights all matrix leds
        """
        self.fill(0)

class BCDDigits(MAX7219_SPI):
    """
    Basic support for display on a 7-Segment BCD display controlled
    by a Max7219 chip using SPI.
    """
    def __init__(self, spi, csPin, nDigits=1):
        self.nDigits = nDigits
        super().__init__(self.nDigits, 8 ,spi ,csPin)

    def init_display(self):
        
        for command, data in (
                    (_SHUTDOWN, 0),
                    (_DISPLAYTEST, 0),
                    (_SCANLIMIT, 7),
                    (_DECODEMODE, (2**self.nDigits)-1),
                    (_SHUTDOWN, 1),
        ):
            self.write_cmd(command, data)        

        self.clearAll()
        self.show()

    def setDigit(self, digit, digitValue):
        """
        set one digit in the display
        param: digit - the display digit zero-based
        param: digitValue - integer ranging from 0->15
        """
        for i in range(4):
            print('digit {} pixel {} value {}'.format(digit,i+4,digitValue & 0x01))
            self.pixel(digit,i,digitValue & 0x01)
            digitValue >>= 1
    
    def setDigits(self, start, digits):
        """
        set the display from a list
        param: start - digit to start display zero-based
        param: digits - list of integer values ranging from 0->15
        """
        for digit in digits:
            print('set digit {} start {}'.format(digit,start))
            self.setDigit(start,digit)
            start += 1

    def setIntDigits(self, start, wide, value):
        """
        start is the start digit position zero based
        param: wide is the number of digits to show/use
        param: value is a number to display
        """
        value = abs(int(value))
        digits = []
        # initialize all digits to blank
        for i in range(wide):
            digits.append(0x0f)
        # initalize a zero digit
        digits[wide-1] = 0x00
        # fill the field with digits right to left
        for i in range(wide):
            if value != 0:                    
                digits[wide-i-1] = value % 10
                value //= 10
        # now send the digits to the display
        self.setDigits(start, digits)        

    def setDot(self,whichDigit, col=None):
        """
        set the decimal point for a digit
        param: whichDigit - the digit to set the decimal point zero-based
        param: col - value > zero lights the decimal point, else unlights the point
        """
        self.pixel(whichDigit,7,col)

    def clearAll(self):
        """
        clear all digits and decimal points
        """
        self.fill(1)
        for i in range(self.nDigits):
            self.setDot(i)

    
