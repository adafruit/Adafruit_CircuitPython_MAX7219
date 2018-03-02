
Introduction
============

.. image :: https://readthedocs.org/projects/adafruit-circuitpython-max7219/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/max7219/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

CircuitPython driver for the MAX7219 LED matrix driver chip.

See `here <https://github.com/adafruit/micropython-adafruit-max7219>`_ for the equivalent MicroPython driver.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Examples
********

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

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_max7219/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

   python3 -m venv .env
   source .env/bin/activate
   pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

   source .env/bin/activate

Then run the build:

.. code-block:: shell

   circuitpython-build-bundles --filename_prefix adafruit-circuitpython-max7219 --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
