
Introduction
============

.. image :: https://readthedocs.org/projects/adafruit-circuitpython-max7219/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/max7219/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MAX7219/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MAX7219/actions/
    :alt: Build Status

CircuitPython driver for the MAX7219 LED matrix driver chip.

See `here <https://github.com/adafruit/micropython-adafruit-max7219>`_ for the equivalent MicroPython driver.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-max7219/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-max7219

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-max7219

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-max7219

Usage Example
=============

adafruit_max7219.Matrix8x8 Example
----------------------------------

.. code-block:: python

      from adafruit_max7219 import matrices
      from board import TX, RX, A2
      import busio
      import digitalio
      import time

      clk = RX
      din = TX
      cs = digitalio.DigitalInOut(A2)

      spi = busio.SPI(clk, MOSI=din)
      display = matrices.Matrix8x8(spi, cs)
      while True:
          display.brightness(3)

          display.fill(1)
          display.pixel(3, 3)
          display.pixel(3, 4)
          display.pixel(4, 3)
          display.pixel(4, 4)
          display.show()
          time.sleep(3.0)

          display.clear_all()
          s = 'Hello, World!'
          for c in range(len(s)*8):
              display.fill(0)
              display.text(s,-c,0)
              display.show()
              time.sleep(0.25)


adafruit_max7219.BCDDigits Example
----------------------------------

.. code-block:: python

      from adafruit_max7219 import bcddigits
      from board import TX, RX, A2
      import bitbangio
      import digitalio

      clk = RX
      din = TX
      cs = digitalio.DigitalInOut(A2)

      spi = bitbangio.SPI(clk, MOSI=din)
      display = bcddigits.BCDDigits(spi, cs, nDigits=8)
      display.clear_all()
      display.show_str(0,'{:9.2f}'.format(-1234.56))
      display.show()

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/max7219/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_max7219/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
