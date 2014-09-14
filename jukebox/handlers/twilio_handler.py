import tornado.web
import jukebox.config
import json

from firebase import firebase

class TwilioHandler(tornado.web.RequestHandler):
    def get(self):
        #self.render("home.html")
        #db = firebase.FirebaseApplication(jukebox.config.FIREBASE_URL)
        #result = db.get("/test", None)
        #self.write('Hello, world!')
        data = json.loads(self.request.body)
        print data


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", TwilioHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

