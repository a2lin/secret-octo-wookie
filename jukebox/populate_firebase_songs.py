from firebase import Firebase
import os
from echonest.remix import audio


INSTRUMENTAL_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'instrumental'))
VOCAL_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'vocal'))

WRITE_TOKEN = "hXMjeLwYHyGMZQiVmNjueFxwvGoGEAZshpNFUNVG"
FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"

song_db = Firebase(FIREBASE_URL + "songs/")

# ff = os.listdir(INSTRUMENTAL_DIR)
# for f in ff:
#     # collect the files
#     if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
#         # file_list.append(os.path.join(directory,f))
#         data = {}
#         data['file_name'] = f
#         data['bpm'] = 140
#         data['RNG'] = 1
#         data['file_type'] = "instrumental"
#         data['start_time'] = 30
#         data['volume'] = 1.0
#         data['song_name'] = f[:-4]
#         # Need to add in ID by hand
#         song_db.post(data)


ff = os.listdir(VOCAL_DIR)
for f in ff:
    # collect the files
    if f.rsplit('.', 1)[1].lower() in ['mp3', 'aif', 'aiff', 'aifc', 'wav']:
        # file_list.append(os.path.join(directory,f))
        data = {}
        data['file_name'] = f
        data['bpm'] = 140
        data['RNG'] = 1
        data['file_type'] = "vocal"
        data['start_time'] = 30
        data['volume'] = 1.0
        data['song_name'] = f[:-4]
        # Need to add in ID by hand
        song_db.post(data)