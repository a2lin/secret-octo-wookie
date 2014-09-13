import tornado.ioloop
import tornado.web
from handlers import MainHandler


def main():
    app = tornado.web.Application(
            [
                (r"/", MainHandler),
            ],
            )
    app.listen(8888);
    tornado.ioloop.IOLoop.instance().start();


if __name__ == "__main__":
    main()
