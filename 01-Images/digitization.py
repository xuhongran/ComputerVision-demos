#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Add this before pyplot otherwise it won't work on openSUSE 15.2
import matplotlib.pyplot as plt

time_of_view = 1 # second
analog_time = np.linspace (0, time_of_view, 1000000) # second

#The original signal
def analog_signal (time_point):
    return np.sin(2 * np.pi * 5 * time_point) + np.cos(2 * np.pi * 11 * time_point)
    # return amplitude * np.cos (2*np.pi*carrier_frequency * time_point + phase)

#The maximum frequency of the signal i.e. cos(2π*fmax*t)
#note: the frequency for sinusoidals is the number of cycles that occur in 2π -> max(2π10/2π, 2π11/2π) = 11
max_signal_frequency   = 11 #determines the oscillations of the original signal;
nyquist_rate = 2 * max_signal_frequency

sampling_frequency = 50 # Hz (1/second)
sampling_period = 1 / sampling_frequency # second
sample_number = int(np.round(time_of_view / sampling_period)) + 1    #Number of samples
sampling_time = np.linspace (0, time_of_view, sample_number)

#Print out the info
print('Maximum signal frequency of analog signal: ' + str(max_signal_frequency))
print('Nyquist rate: ' + str(nyquist_rate))
print('Sampling frequency: ' + str(sampling_frequency))
print('Sampling at {0:.2f}x'.format(sampling_frequency/nyquist_rate) + ' the Nyquist sampling rate.')

#Quantization
max_signal_val = 2 #max value for analog signal, sin and cos are in [-1,1]. we are adding two together so [-2,2]
min_signal_val = -2 #min value for analog signal
val_range = max_signal_val - min_signal_val

quantization_bits     = 8   #number of bits
quantization_num_bins = 2**quantization_bits    #Number of bins on the vertical axis
quantization_step = val_range/(quantization_num_bins-1) #Step size between bins
quantization_bins = []
for i in range(quantization_num_bins):
	quantization_bins.append(min_signal_val + i*quantization_step)
quantization_bins = np.array(quantization_bins)

#Print out the info
print('Quantization bits: ' + str(quantization_bits))
print('Quantization step: ' + str(quantization_step))
print('Number of bins: ' + str(quantization_num_bins))

#Digitization
sampling_signal = analog_signal(sampling_time) #Sample the analog signal at the calculated time points
#scale to 0-1 - for quantization
scale_down_val = (sampling_signal - min_signal_val)/val_range
quantization_bin_indices = list(map(int, np.round(scale_down_val * (quantization_num_bins-1)))) #find the bin index for each value
#get the quantized signal
quantized_signal = quantization_bins[quantization_bin_indices]

#Reconstruction: Whitaker-Shannon interpolation
reconstructed_signal = 0
for i in range(0, sample_number):
    reconstructed_signal += quantized_signal[i] * np.sinc((analog_time-i*sampling_period) / sampling_period)

fig = plt.figure ()
#The analog signal - blue line
plt.plot (analog_time,   analog_signal (analog_time))
#The reconstructed signal - gold line
plt.plot (analog_time, reconstructed_signal)
#The samples - blue circles
plt.stem (sampling_time, sampling_signal, linefmt=':', markerfmt='bo', basefmt='b-', label="samples")
#The quantized samples - red squares
plt.stem (sampling_time, quantized_signal, linefmt='r--', markerfmt='rs', label="quantized samples")
plt.title("Digitization")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

