import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
import wave
import sys

input_file = "test2.wav"
spf = wave.open(input_file,'rb')

# Extract Raw Audio from Wav File
waveform = spf.readframes(-1)
#print waveform
#len(waveform) / 44100 = #seconds in .wav file?
#time = len(waveform) / spf.getframerate()

cpf = len(waveform) / spf.getnframes()
adjusted_sample_rate = spf.getframerate() * cpf

time = len(waveform) / adjusted_sample_rate
#time = len(waveform) / 44100
print "time is " + str(time)
#where 44100 is the frame rate

partition = 10

numCycles = time/partition
print "numCycles is " + str(numCycles)
int1 = 0
int2 = partition

for num in range(1, numCycles):
	if num > 1:
		spf = wave.open(input_file,'rb')
		waveform = spf.readframes(-1)

	vocals = waveform[adjusted_sample_rate*int1 : adjusted_sample_rate*int2]

	spf2 = wave.open('part' + str(num) + '.wav','wb')
	spf2.setparams(spf.getparams())
	spf2.setnframes(len(vocals))
	spf2.writeframes(vocals)

	int1 += partition
	int2 += partition

	spf.close()
	spf2.close()
