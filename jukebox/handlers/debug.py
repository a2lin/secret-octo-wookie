import jukebox.config
import tornado.web

from firebase import firebase

# gets the most recent music location from firebase and writes it out for debug purposes
class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        db = firebase.FirebaseApplication(jukebox.config.FIREBASE_URL)
        result = db.get("/test", None)
        self.write(result)

