import tornado.web

class PlayHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

