import os
import tornado.ioloop
import tornado.web
from jukebox.handlers.main import MainHandler
from jukebox.handlers.debug import DebugHandler
from jukebox.handlers.music_update import MusicUpdateHandler


def main():
    handlers = [
        (r"/update", MusicUpdateHandler),
        (r"/debug", DebugHandler),
        (r"/", MainHandler),
    ]

    settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates")
    )

    application = tornado.web.Application(handlers, **settings)
    application.listen(8888);
    tornado.ioloop.IOLoop.instance().start();


if __name__ == "__main__":
    main()
