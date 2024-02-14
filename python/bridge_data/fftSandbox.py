# Python example - Fourier transform using numpy.fft method

import numpy as np
import matplotlib.pyplot as plt

# How many time points are needed i,e., Sampling Frequency
samplingFrequency   = 100

# At what intervals time points are sampled
samplingInterval = 1 / samplingFrequency

# Begin time period of the signals
beginTime = 0

# End time period of the signals
endTime = 10

# Frequency of the signals
signal1Frequency = 37
signal2Frequency = 12

# Time points
time = np.arange(beginTime, endTime, samplingInterval)

# Create two sine waves
amplitude1 = np.sin(2*np.pi*signal1Frequency*time)
amplitude2 = np.sin(2*np.pi*signal2Frequency*time)

# Create subplot
fig, ax = plt.subplots(2, 1)
plt.subplots_adjust(hspace=0.5)

# Add the sine waves
amplitude = amplitude1 + amplitude2

# Time domain representation of the resultant sine wave
ax[0].set_title('Sine wave with multiple frequencies')
ax[0].plot(time, amplitude)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')

# Frequency domain representation
fourierTransform = np.fft.fft(amplitude)/len(amplitude)           # Normalize amplitude
fourierTransform = fourierTransform[range(int(len(amplitude)/2))] # Exclude sampling frequency

tpCount     = len(amplitude)
values      = np.arange(int(tpCount/2))
timePeriod  = tpCount/samplingFrequency
frequencies = values/timePeriod

# Frequency domain representation
ax[1].plot(frequencies, abs(fourierTransform))
ax[1].set_title('Fourier transform depicting the frequency components')
ax[1].set_xlabel('Frequency')
ax[1].set_ylabel('Amplitude')

plt.show()