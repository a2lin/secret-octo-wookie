# Audio Daemon: this process does the audio processing and stuff like queuing up new files
from threading import Thread
from firebase import Firebase

import time
import random
import json

from jukebox.lib.audio_io import slice_wav
from jukebox.mix import main as mix

WRITE_TOKEN = "hXMjeLwYHyGMZQiVmNjueFxwvGoGEAZshpNFUNVG"
FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"
MIX_DURATION = 30

class AudioDaemon(Thread):
    schedule_table = []

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while(1):
            start_time = time.time()

            songs = self.pick_songs(2);
            files = [self.slice_song(song) for song in songs]
            mashup, key = self.collide_songs(files);


            self.schedule(mashup) 
            sleep(25 - (time.time() - start_time))

    # Return two biased randomly selected song id's from firebase
    def pick_songs(self, count):
        biased_indices = []
        result_songs = []

        songs = Firebase(FIREBASE_URL + "songs").get()

        for song in songs:
           biased_indices += [song["id"]] * song["rng_bias"]

        for i in range(count):
            new_index = biased_indices[int(len(biased_indices) * random.random())]

            result_songs += [new_index]
            biased_indices = [bi for bi in biased_indices if bi is not new_index]

        return result_songs

    # Returns the file name of a song slice 
    def slice_song(self, song_id):
        song = json.load(Firebase(FIREBASE_URL + "songs/" + song_id).get())

        file_name = song['file_name']
        start_time = song['start_time']

        new_file = wavslice + "_" + song_id + "_" + time.time() + ".wav"
        new_path = os.getcwd() + "/../tmp/" + new_file

        slice_wave(file_name, new_path, start_time, start_time + MIX_DURATION) 

    # Collides two wavs file1 and file2. Returns path to crushed file.
    # TODO make better collider
    def collide_songs(self, files):
        target_file = os.getcwd() + "/../static/data/330.wav"
        main(40, files, target_file)
        return target_file

    # TODO make better scheduler
    def schedule(self, file_path):
        key = str(time.time())
        track = Firebase(FIREBASE_URL + "tracks/" + key, auth_token = WRITE_TOKEN)

        track_data = {}
        track_data["file_path"] = file_path
        track_data["offset"] = self.play_time(file_path)

        track.put(json.dump(track_data))

    def play_time(self, file_path):
        last_play = schedule_table[-1] if schedule_table else 0
        new_play = last_play + 25

        schedule_table.append(new_play)
        return new_play
