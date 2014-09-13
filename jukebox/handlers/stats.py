import jukebox.config
import tornado.web

from firebase import firebase

# gets stats out of firebase 
class StatsHandler(tornado.web.RequestHandler):
    def get(self):
        db = firebase.FirebaseApplication(jukebox.config.FIREBASE_URL)
        result = db.get("/test", None)
        self.write(result)

