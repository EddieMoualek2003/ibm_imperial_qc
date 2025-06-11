import os
import struct
import subprocess
import numpy as np
import time
import board
import adafruit_pixelbuf
from adafruit_raspberry_pi5_neopixel_write import neopixel_write

NEOPIXEL = board.D13
num_pixels = 192

class Pi5Pixelbuf(adafruit_pixelbuf.PixelBuf):
    def __init__(self, pin, size, **kwargs):
        self._pin = pin
        super().__init__(size=size, **kwargs)

    def _transmit(self, buf):
        neopixel_write(self._pin, buf)

pixels = Pi5Pixelbuf(NEOPIXEL, num_pixels, auto_write=False, byteorder="RGB", brightness=0.1)




OUTPUT_BIT_FORMAT = "8bit"
BARS_NUMBER = 24
RAW_TARGET = "/dev/stdout"

bytetype, bytesize, bytenorm = ("H", 2, 65535) if OUTPUT_BIT_FORMAT == "16bit" else ("B", 1, 255/8)

def set_bar (pixels, bar, height, color):
    #print (pixels)
    if(bar % 2 == 0):
        for i in range (0, height):
            pixels[(bar * 8) + i] = color
    else:
        for i in range (0, height):
            pixels[(bar + 1) * 8 - (i + 1)] = color

def run():
    # NUM_PIXELS = 216
    # PIXEL_ORDER = neopixel.RGB
    # spi = board.SPI()
    # pixels = neopixel.NeoPixel_SPI(
        # spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False, brightness=0.1
    # )
    process = subprocess.Popen(["cava", "-p", "cavaconfig.txt"], stdout=subprocess.PIPE)
    chunk = bytesize * BARS_NUMBER
    fmt = bytetype * BARS_NUMBER

    if RAW_TARGET != "/dev/stdout":
        if not os.path.exists(RAW_TARGET):
            os.mkfifo(RAW_TARGET)
        source = open(RAW_TARGET, "rb")
    else:
        source = process.stdout
        
    while True:
        data = source.read(chunk)
        if len(data) < chunk:
            break
        sample = [i / bytenorm for i in struct.unpack(fmt, data)]
        sample = np.round(sample, 0)
        pixels.fill(0)
        for i in range(0, 24):
            set_bar(pixels, i, int(sample[i]), 0x0000FF)
        pixels.show()
        print(sample)

if __name__ == "__main__":
    run()