import numpy as np
# import matplotlib.pyplot as plt
from scipy import signal
import wave
import sys

spf = wave.open('test3.wav','rb')
print "commiting suicide now"

# Extract Raw Audio from Wav File
waveform = spf.readframes(-1)
waveform = np.fromstring(waveform, 'Int16')[44100*10 : 44100*20]

# What the fuck am I doing
s_rate = spf.getframerate()
n_rate = s_rate/2
v_l_rate = 100
v_h_rate = 800
v_l_ratio = float(v_l_rate)/n_rate
v_h_ratio = float(v_h_rate)/n_rate

b, a = signal.butter(5, v_h_ratio, 'lowpass')
vocals = signal.filtfilt(b, a, waveform)

spf2 = wave.open('test4.wav','wb')
spf2.setparams(spf.getparams())
spf2.setnframes(len(vocals))
spf2.writeframes(vocals)

spf.close()
spf2.close()

#plt.plot(np.absolute(np.fft.fft(waveform)))
#plt.plot(np.absolute(np.fft.fft(vocals)))
#plt.show()

print "fuck fuck fuck fucking fuck fuck fucking fuck of fucking fuck"
