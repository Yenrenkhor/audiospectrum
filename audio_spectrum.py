import pyaudio
import struct
import numpy as np
import time
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from tkinter import TclError
# %matplotlib tk

CHUNK = 1024 * 2             #samples per frame
FORMAT = pyaudio.paInt16     #audio format (bytes per sample)
CHANNELS = 1                 #single channel for microphone
RATE = 44100                 #samples per second

# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from sample
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
wave = np.arange(0, 2 * CHUNK, 2)  # sound samples (waveform)
spectrum = np.linspace(0, RATE, CHUNK)  # frequency (spectrum)

# create a line object with random data
line, = ax1.plot(wave, np.random.rand(CHUNK), '-', lw=2)

# create a line object with random data
line_spectrum, = ax2.semilogx(spectrum, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for the axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# format spectrum axes
ax2.set_xlim(20, RATE / 2)

plt.show(block=False)
print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:

    # binary data
    data = stream.read(CHUNK)

    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128

    line.set_ydata(data_np)

    # compute FFT and update line
    yf = fft(data_int)
    line_spectrum.set_ydata(np.abs(yf[0:CHUNK]) * 2 / (256 * CHUNK))

    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1

    except TclError:

        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)

        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break