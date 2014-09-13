import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import jukebox.application

from jukebox.handlers.main import MainHandler
from jukebox.handlers.debug import DebugHandler
from jukebox.handlers.music_update import MusicUpdateHandler


def main():
    application = jukebox.application.Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)

    tornado.ioloop.IOLoop.instance().start();


if __name__ == "__main__":
    main()
