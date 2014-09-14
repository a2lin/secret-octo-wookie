import jukebox.config
import tornado.web

# gets the most recent music location from firebase and writes it out for debug purposes
class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        pass
