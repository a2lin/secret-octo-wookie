import os
import tornado.web

from jukebox.handlers.play import PlayHandler
from jukebox.handlers.stats import StatsHandler

from jukebox.handlers.home import HomeHandler

from jukebox.handlers.debug import DebugHandler
from jukebox.handlers.music_update import MusicUpdateHandler

from jukebox.handlers.twilio_handler import TwilioHandler

class Application(tornado.web.Application):
    def __init__(self):
        # the current list of tracks that are playable
        self.music = []

        handlers=[
            (r"/play", PlayHandler),
            (r"/stats", StatsHandler),
            (r"/twilio", TwilioHandler),
            #TODO remove update and debug
            (r"/update", MusicUpdateHandler),
            (r"/debug", DebugHandler),
    
            (r"/", HomeHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
        )

        tornado.web.Application.__init__(self, handlers, **settings)
