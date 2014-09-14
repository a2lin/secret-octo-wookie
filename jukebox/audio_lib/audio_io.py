import wave
import sys

# Slice up a wav file
def slice_wav(in_file, out_file, start_time, stop_time):
    # Open file
    spf = wave.open(in_file, 'r')
    waveform = spf.readframes(-1)

    # Adjust for stereo vs. mono encoding
    cpf = len(waveform) / spf.getnframes()
    adjusted_sample_rate = spf.getframerate() * cpf

    start_index = adjusted_sample_rate * start_time
    stop_index = adjusted_sample_rate * stop_time

    truncated_wave = waveform[start_index:stop_index]

    # Create and to new file, preserving most params
    f = open(out_file,'a')
    f.close()

    spf2 = wave.open(out_file,'w')

    spf2.setparams(spf.getparams())
    spf2.setnframes(len(truncated_wave) / adjusted_sample_rate)
    spf2.writeframes(truncated_wave)

    spf.close()
    spf2.close()
