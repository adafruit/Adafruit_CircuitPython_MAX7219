from distutils.core import setup


setup(
    name='micropython-adafruit-max7219',
    py_modules=['max7219'],
    version="1.0",
    description="Driver for MicroPython for the MAX7219 LED matrix.",
    long_description="""\
Driver for a single MAX7219-based LED matrix.""",
    author='Radomir Dopieralski',
    author_email='micropython@sheep.art.pl',
    classifiers = [
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
