#wav should contain the location of the wav file
#script will create myfile.wav.mp3 in the same directory as .wav
wav = 'myfile.wav'
cmd = 'lame --preset insane %s' % wav
subprocess.call(cmd, shell=True)
