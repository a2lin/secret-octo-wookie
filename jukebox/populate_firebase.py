# Script for putting song attributes into firebase for lookup
# Paths are hard-coded to match Jonathan's computer
from firebase import Firebase
import os
from echonest.remix import audio

INSTRUMENTAL_DIR = "/home/juesato/Music/Instrumental"
VOCAL_DIR = "/home/juesato/Music/Vocal"

WRITE_TOKEN = "hXMjeLwYHyGMZQiVmNjueFxwvGoGEAZshpNFUNVG"
FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"

#### UNCOMMENT FOR INSTRUMENTAL ####
similarity_instrumental = Firebase(FIREBASE_URL + "similarity_instrumental/")
data = []

ff = os.listdir(INSTRUMENTAL_DIR)
for f in ff:
    # collect the files
    if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
        # file_list.append(os.path.join(directory,f))
        file_path = os.path.join(INSTRUMENTAL_DIR, f)
        song = audio.LocalAudioFile(file_path).analysis
        song_feats = {}
        song_feats['loudness'] = song.loudness
        song_feats['tempo'] = song.tempo.get('value')
        song_feats['name'] = f.rsplit('.',1)[0]
        data.append(song_feats)

similarity_instrumental.post(data)

#################### COPY PASTED ##################
# similarity_vocal = Firebase(FIREBASE_URL + "similarity_vocal/")
# data = []

# ff = os.listdir(VOCAL_DIR)
# for f in ff:
#     # collect the files
#     if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
#         # file_list.append(os.path.join(directory,f))
#         file_path = os.path.join(VOCAL_DIR, f)
#         song = audio.LocalAudioFile(file_path).analysis
#         song_feats = {}
#         song_feats['loudness'] = song.loudness
#         song_feats['tempo'] = song.tempo.get('value')
#         song_feats['name'] = f.rsplit('.',1)[0]
#         data.append(song_feats)

# similarity_vocal.post(data)
