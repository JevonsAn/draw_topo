import tornado.httpserver
import tornado.web
import tornado.ioloop
import os
import random
import math
import json
from build_topo import build_dict, build_dict2, build_dict3

global_values = {"topo_json": ""}


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        with open("force_directed_graph.html", encoding="utf8") as f:
            content = f.read()
        self.write(content)


class JsonHandler(tornado.web.RequestHandler):

    def get(self):
        asn = self.get_argument("asn")
        topo_json = ""
        if asn.isdigit():
            json_type = self.get_argument("type")
            # d = build_dict(int(asn))
            if json_type == "1":
                d = build_dict2(int(asn))
                topo_json = json.dumps(d)
            elif json_type == "0":
                d = build_dict(int(asn))
                topo_json = json.dumps(d)
            elif json_type == "2":
                d = build_dict3(int(asn))
                topo_json = json.dumps(d)
            # print(len(topo_json))
        self.write(topo_json)


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    application = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/json", JsonHandler),
            # (r"/search", SearchHandler),
            # (r"/relation", RelationHandler),
            # (r"/country", CountryHandler),
            # (r"^/.*$", OtherHandler),
            # (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/auto/bgpsim/web"})
        ],
        debug=True,
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(application)
    # http_server.bind(65530)
    # http_server.start(0)
    http_server.listen(6789)
    tornado.ioloop.IOLoop.instance().start()
