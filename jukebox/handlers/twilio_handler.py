import tornado.web
import jukebox.config
import json
import os
from firebase import Firebase

FIREBASE_URL = "https://blazing-fire-4446.firebaseio.com/"
METADATA_URL = "https://blazing-fire-4446.firebaseio.com/metadata/"
class TwilioHandler(tornado.web.RequestHandler):
    def get(self):
        db = Firebase(os.path.join(jukebox.config.FIREBASE_URL, "songs")).get()
        self.bodyData = self.get_argument('Body', True)

	if self.bodyData.lower() == 'faster':
        print "FASTERRRRRRRRRRRRRRRRRRRRRRR"
	    self.increase_speed()
	elif self.bodyData.lower() == 'slower':
	    self.decrease_speed()
	elif self.bodyData.lower() == 'louder':
	    self.increase_volume()
	elif self.bodyData.lower() == 'quieter':
	    self.decrease_volume()
	else:
	    self.consider_suggestions()

    # input change methods 
    def increase_speed(self):
        # speed = Firebase(METADATA_URL + "bpm").get()
        # speedRef = Firebase(METADATA_URL + "bpm")
        # speedRef.update(speed + 20)
        cur_speed = Firebase(FIREBASE_URL + 'cur_speed/')
        bpm = cur_speed.get()['bpm']
        cur_speed.update({'bpm':bpm, 'dbpm':20})

    def decrease_speed(self):
        # speed = Firebase(METADATA_URL + "bpm").get()
        # speedRef = Firebase(METADATA_URL + "bpm")
        # speedRef.update(speed - 20)
        cur_speed = Firebase(FIREBASE_URL + 'cur_speed/')
        bpm = cur_speed.get()['bpm']
        cur_speed.update({'bpm':bpm, 'dbpm':-20})

    def increase_volume(self):
        volume= Firebase(METADATA_URL + "volume").get()
        volRef = Firebase(METADATA_URL + "volume")
        volRef.update(volume + 0.2)

    def decrease_volume(self):
        volume= Firebase(METADATA_URL + "volume").get()
        volRef = Firebase(METADATA_URL + "volume")
        volRef.update(volume - 0.2)

    def consider_suggestions(self):
        body = self.bodyData.split(" ")
        next_song = Firebase(FIREBASE_URL + 'next_song/')
        if len(body) == 2 and body[0].lower() == 'vocal':
            print "NEW VOCALS YEAH"
            next_song.update({'must_play':1, 'song_name': body[1].lower(), 'song_type': 'vocal'})
            return
        elif len(body) == 2 and body[0].lower() == 'instrumental':
            next_song.update({'must_play':1, 'song_name': body[1].lower(), 'song_type': 'instrumental'})
            return

        res = Firebase("https://blazing-fire-4446.firebaseio.com/songs/" + self.bodyData + "/").get()
        #print res
        if not res:
            curFB = Firebase("https://blazing-fire-4446.firebaseio.com/songs/")
            curFB.push({'RNG':1, 'file_name':"testFN", 'file_type':"instrumental", 'id':self.bodyData, 'song_name':"testFN", 'start_time':30})
        else:
            curRNG = Firebase("https://blazing-fire-4446.firebaseio.com/songs/" + self.bodyData + "/RNG/").get()
            print curRNG
            curRNG = curRNG + 1
            print curRNG
            rngREF = Firebase("https://blazing-fire-4446.firebaseio.com/songs/" + self.bodyData + "/")
            rngREF.update({"RNG": curRNG})		
