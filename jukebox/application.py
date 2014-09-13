import os
import tornado.web

from jukebox.handlers.main import MainHandler
from jukebox.handlers.debug import DebugHandler
from jukebox.handlers.music_update import MusicUpdateHandler


class Application(tornado.web.Application):
    def __init__(self):
        # the current list of tracks that are playable
        self.music = []

        handlers=[
            (r"/update", MusicUpdateHandler),
            (r"/debug", DebugHandler),
            (r"/", MainHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
        )

        tornado.web.Application.__init__(self, handlers, **settings)
