import jukebox.config
import tornado.web

from firebase import firebase

# updates firebase with new details upon receipt
class MusicUpdateHandler(tornado.web.RequestHandler):
    def get(self):
        db = firebase.FirebaseApplication(jukebox.config.FIREBASE_URL)
        try:
            music_loc = self.get_argument("location")
            if music_loc:
                result = db.put("/test", "loc", music_loc)
        except tornado.web.MissingArgumentError:
            pass

