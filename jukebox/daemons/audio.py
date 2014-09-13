# Audio Daemon: this process does the audio processing and stuff like queuing up new files
from threading import Thread
from jukebox.lib.audio_io import slice_wav
from jukebox.lib.mix import main as mix

import firebase import Firebase
import time
import random
import json

WRITE_TOKEN = "hXMjeLwYHyGMZQiVmNjueFxwvGoGEAZshpNFUNVG"
FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"
MIX_DURATION = 30

class AudioDaemon(Thread):
    schedule_table = []

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while(true):
            start_time = time.time()

            songs = pick_songs(self, 2);
            files = [slice_song(song) for song in songs]
            mashup, key = collide_songs(files);


            schedule(mashup) 
            sleep(25 - (time.time() - start_time))

    # Return two biased randomly selected song id's from firebase
    def pick_songs(self, count):
        biased_indices = []
        result_songs = []

        songs = Firebase(FIREBASE_URL + "songs").get()

        for song_id in songs:
           biased_indices += [songs_id] * songs[song_id]["rng_bias"]

        for i in range(len(count)):
            new_index = biased_indices[len(biased_indices) * random.random()]

            result_songs += [new_index]
            biased_indices = [bi for bi in biased_indices if bi is not new_index]

        return result_songs

    # Returns the file name of a song slice 
    def slice_song(song_id):
        song = Firebase(FIREBASE_URL + "songs/" + song_id).get()

        file_name = song['file_name']
        start_time = song['start_time']

        new_file = wavslice + "_" + song_id + "_" + time.time() + ".wav"
        new_path = os.getcwd() + "/../tmp/" + new_file

        slice_wave(file_name, new_path, start_time, start_time + MIX_DURATION) 

    # Collides two wavs file1 and file2. Returns path to crushed file.
    def collide_songs(file1, file2):
        # TODO fix this
        return os.getcwd() + "/../static/data/330.wav"

    # TODO make better scheduler
    def schedule(file_path):
        key = str(time.time())
        track = Firebase(FIREBASE_URL + "tracks/" + key, auth_token = WRITE_TOKEN)

        track_data = {}
        track_data["file_path"] = file_path
        track_data["offset"] = play_time(file_path)

        track.put(json.dump(track_data))

    def play_time(file_path):
        last_play = schedule_table[-1] if schedule_table else 0
        new_play = last_play + 25

        schedule_table.append(new_play)
        return new_play
