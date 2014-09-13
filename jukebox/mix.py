#!/usr/bin/env python
# encoding: utf=8

"""
multitest.py

Take a whole directory of audio files and smash them together, by
beat, with a fairly simple algorithm.
"""

import os, sys
import time
from math import sqrt
import dirac

from echonest.remix import audio, modify
import numpy as np
from collections import Counter

usage = """
Usage: 
    python mix.py <inputDirectory> <outputFilename> <beats>

Example:
    python mix.py ../music mashedbeats.mp3 40
"""

def keyshift(main_key, song_key):
    keyshift = main_key - song_key
    if keyshift < -6:
        keyshift += 12
    if keyshift > 6:
        keyshift -= 12
    return keyshift

def main(num_beats, file_names, outfile):
    # file_names is an array of file names
    aud = []
    for file_path in file_names:
        aud.append(audio.LocalAudioFile(file_path))
    num_files = len(aud)
    x = audio.AudioQuantumList()
    
    print >> sys.stderr, "Assembling beats.",

    volume_norm = []
    aud = sorted(aud, key=lambda a: a.analysis.loudness, reverse=True) # Sort from softest to loudest.
    first_track = aud[0].analysis
    main_key = first_track.key.get('value')

    for track in aud:
        volume_norm.append(first_track.loudness / track.analysis.loudness) # This isn't right but I don't want to deal with decibels

    # print "Volume norm:", volume_norm

    aligned_beats = []
    for track in aud:
        section_lengths = []
        song = track.analysis
        sections = song.sections
        for section in sections:
            bars = section.children()
            section_lengths.append(len(bars))


        # Find some regularly repeating section length, call this section the chorus. We'll start the track here
        mode = Counter(section_lengths).most_common(1)
        # print "MODE", mode[0][0]
        beats_from_chorus = []
        start = False
        for section in sections:
            if len(section.children()) == mode[0][0]:
                start = True
            if start:
                bars = section.children()
                for bar in bars:
                    for beat in bar.children():
                        beats_from_chorus.append(beat)
        aligned_beats.append(beats_from_chorus)


    modifier = modify.Modify()
    for w in range(num_beats):
        print >> sys.stderr, '.',
        curbeats = []
    
        desired_dur = first_track.beats[w%len(first_track.beats)].duration
        for track, beats, norm in zip(aud, aligned_beats, volume_norm):
            song = track.analysis
            b = beats[w%len(beats)]
            b_audio = b.render()

            # modifier.shiftPitchSemiTones(b_audio, semitones=keyshift(main_key, song.key.get('value'))) # Fix pitch
            scaled_beat = dirac.timeScale(b_audio.data, desired_dur * 1.0 / b.duration) # Fix duration for smoothing
            scaled_beat *= norm # Normalize volume

            ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape, sampleRate=aud[0].sampleRate, numChannels=scaled_beat.shape[1])
            curbeats.append(ts)
        
        x.append(audio.Simultaneous(curbeats))
    
    print >> sys.stderr, "\nStarting rendering pass..."
    
    then = time.time()
    # call render_sequentially() with no arguments, and then it calls itself with
    #  contextual arguments for each source, for each AudioQuantum. It's a lot of
    #  tree-walking, but each source file gets loaded once (and takes itself from)
    #  memory when its rendering pass finishes.
    x.render().encode(outfile)
    
    print >> sys.stderr, "%f sec for rendering" % (time.time() - then,)

if __name__ == '__main__':
    try:
        directory = sys.argv[-3]
        outfile = sys.argv[-2]
        num_beats = int(sys.argv[-1])

        file_list = []
        ff = os.listdir(directory)
        for f in ff:
            # collect the files
            if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
                file_list.append(os.path.join(directory,f))
    except:
        print usage
        sys.exit(-1)
    main(num_beats, file_list, outfile)

