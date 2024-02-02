# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:16:29 2023

@author: Doug
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from scipy.signal import iirfilter, lfilter, butter, medfilt
import mplcursors

# Step 1: Read the CSV file
data = pd.read_csv('D:\Downloads\inqb8.csv')
column_2_data = data.iloc[:, 1].values  # Assuming the first column is index 0
column_2_data_average = np.average(column_2_data)
column_2_data = column_2_data - column_2_data_average

# Step 2: Compute the FFT
fft_values = np.fft.fft(column_2_data)
frequencies = np.fft.fftfreq(len(fft_values), 1/199)  # 1/200 is the time interval for 200Hz

# Filter the data
nyquist = 0.5 * 200  # Nyquist frequency, half of the sampling rate
low = 7 / nyquist  # Normalize by Nyquist frequency
high = 12 / nyquist  # Normalize by Nyquist frequency
lowpassCutoff = .75/nyquist

#b, a = iirfilter(N=5, Wn=[low, high], btype='bandstop', ftype='butter')

b, a = butter(N=5, Wn=lowpassCutoff, btype='low')

# Step 3: Apply the filter
butter_filtered_data = lfilter(b, a, column_2_data)

# Median Filter
median_filtered_data = medfilt(column_2_data, kernel_size=75)

# Step 3: Plot the magnitude spectrum
plt.figure(figsize=(8, 3))
plt.plot(frequencies, np.abs(fft_values), linewidth=0.5)  # Set line width to 0.5
plt.title('FFT of Column 2 Data')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.xlim([0, 100])  # Set x-axis limits to 0-100Hz
plt.ylim([-1, 2])  # Set x-axis limits to 0-100Hz
plt.xticks(np.arange(0, 101, 5)) 
plt.grid(True)
plt.show()



# plt.figure(figsize=(8, 4))
# plt.plot(column_2_data, label='Original Data', linewidth=0.2)
# plt.plot(filtered_data, label='Filtered Data', linewidth=0.5)
# plt.title('Original vs Filtered Data')
# plt.xlabel('Sample Number')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.grid(True)
# plt.show()

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(column_2_data, label='Original Data', linewidth=0.5)
ax.plot(butter_filtered_data, label='Butterworth Filtered Data', linewidth=0.5)
ax.plot(median_filtered_data, label='Median Filtered Data', linewidth=0.5)
ax.set_title('Original vs Filtered Data')
ax.set_xlabel('Sample Number')
ax.set_ylabel('Amplitude')
ax.legend()
ax.grid(True)

# Step 6: Enable mplcursors
mplcursors.cursor(hover=True)

plt.show()