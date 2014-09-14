import tornado.web
import jukebox.config
import json
import os
from firebase import Firebase

class TwilioHandler(tornado.web.RequestHandler):
    def get(self):
        #self.render("home.html")
        db = Firebase(os.path.join(jukebox.config.FIREBASE_URL, "songs")).get()
        #result = db.get("/test", None)
        #self.write('Hello, world!')
        self.bodyData = self.get_argument('Body', True)
	#print bodyData

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


    def increase_speed(self):
        #TODO XANDER'S CODE
        print 'speed is increasing'
    def decrease_speed(self):
        #TODO XANDER'S CODE
        print 'speed is decreasing'
    def increase_volume(self):
        #TODO XANDER'S CODE
        print 'getting louder'
    def decrease_volume(self):
        #TODO Xander's code
        print 'getting quieter'
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
	#print 'analyzing suggestions'
