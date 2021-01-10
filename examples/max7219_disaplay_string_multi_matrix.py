# Display string on multi led matrix at any position
# Author: songjiangzhang@hotmail.com
# This sample use EPS32 S2 Board

from adafruit_max7219 import matrices
import board
import busio
import digitalio

clk = board.IO4
din = board.IO2
cs = digitalio.DigitalInOut(board.IO3)

spi = busio.SPI(clk, MOSI=din)
display = matrices.Matrix8x8(spi, cs,4)
display.framebuf.rotation =1  # rotate screen 

display.clear_all()
while True:
    display.display_str('abc7568123456789asdfghj',2)
