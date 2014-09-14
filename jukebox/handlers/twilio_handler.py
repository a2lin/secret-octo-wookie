import tornado.web
import jukebox.config
import json
import os
from firebase import Firebase

METADATA_URL = "https://blazing-fire-4446.firebaseio.com/metadata/"
class TwilioHandler(tornado.web.RequestHandler):
    def get(self):
        db = Firebase(os.path.join(jukebox.config.FIREBASE_URL, "songs")).get()
        self.bodyData = self.get_argument('Body', True)

	if self.bodyData.lower() == 'faster':
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
        speed = Firebase(METADATA_URL + "bpm").get()
	speedRef = Firebase(METADATA_URL + "bpm")
        speedRef.update(speed + 20)

    def decrease_speed(self):
        speed = Firebase(METADATA_URL + "bpm").get()
	speedRef = Firebase(METADATA_URL + "bpm")
        speedRef.update(speed - 20)

    def increase_volume(self):
        volume= Firebase(METADATA_URL + "volume").get()
	volRef = Firebase(METADATA_URL + "volume")
        volRef.update(volume + 0.2)

    def decrease_volume(self):
        volume= Firebase(METADATA_URL + "volume").get()
	volRef = Firebase(METADATA_URL + "volume")
        volRef.update(volume - 0.2)

    def consider_suggestions(self):
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
