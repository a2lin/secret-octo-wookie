# Audio Daemon: this process does the audio processing and stuff like queuing up new files
from threading import Thread
from firebase import Firebase

import time
import random
import os

import jukebox.audio_lib.audio_io
import jukebox.mix

WRITE_TOKEN = "hXMjeLwYHyGMZQiVmNjueFxwvGoGEAZshpNFUNVG"
FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"
MIX_DURATION = 30
CROSSFADE_TIME = 5

class AudioDaemon(Thread):
    def __init__(self):
        self.schedule_table = []
        self.bpm = 140

        Thread.__init__(self)

    def run(self):
        while(1):
            start_time = time.time()

            # grab user input - bpm +-, next song, and whatnot

            (vo, bg) = self.get_next();
            mashup = self.render_next(vo, bg);
            self.schedule(mashup) 

            time.sleep(MIX_DURATION - CROSSFADE_TIME - int(time.time() - start_time))

    ##### MAIN CONTROL FLOW
    def get_next(self):
        songs = Firebase(FIREBASE_URL + "songs").get()

        vo_ids = []
        bg_ids = []

        for song_id in songs:
            song = songs[song_id]
            if song["file_type"] == "instrumental":
                bg_ids += [song["id"]] 
            else:
                vo_ids += [song["id"]] 

        vo_id = vo_ids[int(len(vo_ids) * random.random())]
        bg_id = bg_ids[int(len(bg_ids) * random.random())]

        vo_clip = self.slice_song(vo_id)
        bg_clip = self.slice_song(bg_id)

        return (vo_clip, bg_clip)

    def render_next(self, vocals, background):
        name = str(int(time.time()))
        target_file = os.path.join(os.getcwd(), "jukebox/static/data/" + name + ".wav")

        beat_count = self.bpm * MIX_DURATION / 60
        jukebox.mix.mix_tracks(beat_count, [vocals, background], target_file, self.bpm)

        return target_file

    def schedule(self, file_path):
        track = Firebase(FIREBASE_URL + "tracks/")

        track_data = {}
        track_data["url"] = file_path.replace(os.path.join(os.getcwd(), "jukebox"), "")
        track_data["offset"] = self.play_time(file_path)

        track.post(track_data)

    ##### HELPER METHODS
    def slice_song(self, song_id):
        song = Firebase(FIREBASE_URL + "songs/" + song_id).get()

        # Assemble fiels from relative paths
        file_name = song['file_name']
        file_type = song['file_type']
        old_path = os.path.join(os.getcwd(), "data", file_type, file_name)

        new_file = "slice_wav_" + song_id + "_" + str(time.time()) + ".wav"
        new_path = os.path.join(os.getcwd(), "data/clips/" , new_file)

        # Overcorrect because we don't know how many beats there are
        start_time = song['start_time']
        jukebox.audio_lib.audio_io.slice_wav(old_path, new_path, start_time, start_time + MIX_DURATION*2)

        return new_path

    def play_time(self, file_path):
        # Use UNIX times so javascript can discard songs in the past
        last_play = self.schedule_table[-1] if self.schedule_table else int(time.time())
        new_play = last_play + 25

        self.schedule_table.append(new_play)
        return new_play
