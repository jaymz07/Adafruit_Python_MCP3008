# Author: James Bounds
# License: Public Domain

# Rudimentary Oscilloscope (if you could call it that).
# Plots Voltage vs time using the matplotlib library.
# Note that matplotlib and associated requirements must be installed

# This is also a test of the acquistion speeds available using this library.
# On my Raspberry Pi, I get ~12K Samples per second.
# This is pretty dismal compared to a 44K samples per second
# sound card.
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


import matplotlib.pyplot as plt
import numpy as np

#Constants for voltage estimate
railVoltage = 3.325
adcQuantizations = 2**10 #10 Bit Chip
convFactor = railVoltage/adcQuantizations

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE,max_speed_hz = 3900000))
#Note that we have set the clock speed higher than the stock examples.
#The ADC chip datasheet quotes a 3.9MHz Clock speed if Vdd is set to 5V.
#The closest convenient SPI frequency is 3.9MHz

#Lists keeping track of data coming from ADC as well as time stamps
graph_t, graph_y = [],[]

#Start time
t0 = time.time()

print('Reading MCP3008 values, press Ctrl-C to quit...')

# Main program loop.

try:
    while True:
        # Read all the ADC channel values in a list.
        values = [0]*8
#        for i in range(8):
#            # The read_adc function will get the value of the specified channel (0-7).
#            values[i] = mcp.read_adc(i)

        #Note that we are only reading from one channel here (ch 0)
        values[0] = mcp.read_adc(0)
        values[1] = mcp.read_adc_difference(0)
        
        #Append values to lists for later plotting.
        graph_t.append(time.time() - t0)
        graph_y.append(values)

# Catch Exception thrown by Crtl-C and plot        
except KeyboardInterrupt:
    plt.plot(graph_t,np.array(graph_y)[:,0]*convFactor)
    plt.plot(graph_t,np.array(graph_y)[:,1]*convFactor)
    N = len(graph_t)
    strFormat = (N, graph_t[-1]*1000, N/graph_t[-1])
    #print sample rate achieved.
    print("Collected %d samples in %.2f ms (%.2f samples per sec)" % strFormat )
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.show()    
