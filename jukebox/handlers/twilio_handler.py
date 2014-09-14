import tornado.web
import jukebox.config
import json

from firebase import Firebase

class TwilioHandler(tornado.web.RequestHandler):
    def get(self):
        #self.render("home.html")
        #db = firebase.FirebaseApplication(jukebox.config.FIREBASE_URL)
        #result = db.get("/test", None)
        #self.write('Hello, world!')
        data = json.loads(self.request.body)
        print data
