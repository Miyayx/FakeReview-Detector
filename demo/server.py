import os
import os.path
import re
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.web import StaticFileHandler

from tornado.options import define,options

import sys
sys.path.append("/home/yang/GraduationProject/")
import fake_detector

define("port",default=12345,help="run on the given port",type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            title = u"Fake-Detector",
            template_path = os.path.join(os.path.dirname(__file__),"UI"),
            static_path = os.path.join(os.path.dirname(__file__),"UI")
                )

        handlers = [
            (r"/",MainHandler),
            (r"/detect",DetectHandler),
            (r"/(review\.json)",StaticFileHandler,{'path':settings["static_path"]}),
            (r"/(img/.*)",StaticFileHandler,{'path':settings["static_path"]}),
            (r"/(css/.*)", StaticFileHandler, {'path': settings["static_path"]}),
            (r"/(js/.*)", StaticFileHandler, {'path': settings["static_path"]}),
        ]

        tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        print "MainHandler"

class DetectHandler(tornado.web.RequestHandler):
    def get(self):
        string = self.get_argument("string",None)
        print string
        if string:
            if "." in string and string.split(".")[1] in ["csv","csv2"]:
                string =  os.popen("find /home/yang/GraduationProject/data/ -name %s"%string).read().strip('\n')
                print string
            result = fake_detector.fake_detect_pipeline(string)
            self.write(result)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
