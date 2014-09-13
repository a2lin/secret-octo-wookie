import os
import tornado.ioloop
import tornado.web
from handlers.main import MainHandler


def main():
    handlers = [
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
