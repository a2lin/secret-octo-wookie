from echonest.remix import audio
from firebase import Firebase
import math

FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"

def similarity_score(tempo1, tempo2, loud1, loud2):
    # These scores are not normalized at all, but higher score means more similar
    # Scores are all <= 0.0
    return (-1 * abs(math.log(tempo1 / tempo2)) + abs(loud1 - loud2) * -.01) 

def get_similar_tracks(track_file, vocal=True):
    song = audio.LocalAudioFile(track_file).analysis
    loudness = song.loudness
    tempo = song.tempo.get('value')
    # print loudness, tempo
    similar_apps = []
    if vocal:
        available_vocals = Firebase(FIREBASE_URL + "similarity_vocal/-JWmru64YOAUqDvolxmN/").get()
        for track in available_vocals:
            score = similarity_score(tempo, track['tempo'], loudness, track['loudness'])
            similar_apps.append((track['name'], score))
    else:
        available_instrumentals = Firebase(FIREBASE_URL + "similarity_instrumental/-JWmsMSK8HK7KbUY6m_6/").get()
        for track in available_instrumentals:
            score = similarity_score(tempo, track['tempo'], loudness, track['loudness'])
            similar_apps.append((track['name'], score))

    similar_apps = sorted(similar_apps, key=lambda x: x[1], reverse=True)
    return similar_apps[:3]

track_file = "/home/juesato/Music/Instrumental/Rude.mp3"
print get_similar_tracks(track_file, vocal=False)