# Boiled down code. Bypasses the Adafruit library and uses
# spidev directly. Can obtain approximately 5X higher sample rate
# than putting the Adafruit's read_adc() in a loop.

# Further increases of sample rate now require modification of the spidev library.
# --->Need function that loops the xfer2() command for a constant query.
# --->Speed limitation is now the number of operations that occur inside of xfer2()

import spidev
import time

device = spidev.SpiDev()
device.open(0,0)

device.max_speed_hz = 4000000
device.mode = 0
device.cshigh = False
device.lsbfirst = False

adc_number=0
# Build a single channel read command.
# For example channel zero = 0b11000000
command = 0b11 << 6                  # Start bit, single channel read
command |= (adc_number & 0x07) << 3

N = 100000
output = [0.0]*N
timeStart = time.time()
for i in range(0,N):
    output[i] = (device.xfer2([command, 0x0, 0x0]))
timeEnd = time.time()
print("%f Samples per second" % (N/(timeEnd-timeStart)))