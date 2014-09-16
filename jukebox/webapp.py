import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import jukebox.application

from jukebox.daemons.audio import AudioDaemon

def main():
    # AudioDaemon does the music processing
    ad = AudioDaemon()
    ad.start()
    # start the web app
    application = jukebox.application.Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start();

if __name__ == "__main__":
    main()
