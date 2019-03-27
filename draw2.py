import tornado.web
import tornado.ioloop
import os
import random
import math
import json
import base64
from io import BytesIO
import gzip

from info import get_info, get_relations, get_prefix_tree, p_list  # citys,

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}
# x_scale = [638, 2032, 2541, 778, 476, 2639, 928, 607, 974, 1192, 267]  # [800, 4167, 3378, 1519, 1260, 3530, 2473, 1830, 2276, 2988, 700]
# x_width = [x / sum(x_scale) * 1200 for x in x_scale]
# x_list = [100 + sum(x_width[:i]) for i in range(len(x_width) + 1)]
# p_list = [-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
du_list = ['%d° W' % i for i in p_list[:5]] + ["0° "] + ['%d° E' % i for i in p_list[6:]]

# x_scale = [766, 1114, 4167, 3378, 1519, 1260, 3530, 2473, 1830, 2276, 2988, 1370]
# # [2.2, 10, 10, 5, 6, 9, 4, 4, 4, 4, 1.6]  # [3,3,3,3,3,3,3,3,3,3,3,3] #
# x_width = [x / sum(x_scale) * 1200 for x in x_scale]
# x_list = [100 + sum(x_width[:i]) for i in range(len(x_width) + 1)]
# p_list = [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
# du_list = ['%d° W' % i for i in p_list[:5]] + ["0° "] + ['%d° E' % i for i in p_list[6:]]

# rects = []

lines = []
relationship = get_relations()
rtree = get_prefix_tree()


def calc_posi(lgt, x_list, x_width):
    t = len(p_list) - 2
    for i in range(len(p_list) - 1):
        if p_list[i] <= lgt < p_list[i + 1]:
            t = i
            break
    base = x_list[t]
    width = lgt - p_list[t]
    real_width = width / (p_list[t + 1] - p_list[t]) * x_width[t]
    return base + real_width


def rect_posi(tier1_asns, tier2_asns, asn_leafs, x_list, x_width):
    rects = []
    lgtss = []
    # lines = []
    dots = []
    circles = []
    tier2_rects = []
    yax_key = [0]
    yax_value = [0]

    thigh = 50
    nnn = 0
    # print([t['scale'] for t in asns])
    # tier1_asns.sort(key=lambda As: int(As['scale']), reverse=True)
    # print(tier1_asns)
    for asn in tier1_asns:
        t1 = 3
        t2 = 0
        high = math.log(int(asn["scale"])) * t1 + t2
        a = {
            "asn": int(asn["asn"]),
            "yp": thigh + 1,
            "height": high,
            "name": "%s, %s, %s" % (asn["asn"], asn["name"], asn["country"]),  # f'{asn["asn"]}, {asn["name"]}, {asn["country"]}',
            "scale": asn["scale"],
            "color": asn["color"]
        }
        dark_color = asn["dark_color"]
        nnn += 1
        yax_key.append(thigh + high - 50)
        yax_value.append(nnn)

        # a["color"], dark_color = rand_color()
        thigh += high
        for rx in asn["rects"]:
            b = {x: y for x, y in a.items()}
            b["xp"] = calc_posi(rx[0], x_list, x_width)
            b["width"] = calc_posi(rx[1], x_list, x_width) - b["xp"]
            rects.append(b)

        # lgts = asn["posis"]
        # for l in lgts:
        #     lgtss.append({"xp": calc_posi(l, x_list, x_width), "yp": a["yp"], "width": 2,
        #                   "color": dark_color, "height": a["height"] - 3, "lgt": l})

        prefixs = sorted(asn["prefixs"], key=lambda x: float(x[0]))
        # prefixs.sort(key=lambda x: x[0])
        for c in prefixs:
            prefix = " "
            leng = math.log2(float(c[1]))
            leng = leng if leng <= 24 else 24
            r = (high / 2 - 4) / 26 * leng + 2
            try:
                pl = calc_posi(float(c[0]), x_list, x_width)
            except Exception as e:
                print(c[0])
                continue

            circles.append({"xp": "%.1f" % pl, "yp": thigh - high / 2, "r": r, "asn": int(asn["asn"]), "len": str(24 - leng)[:4], "color": dark_color, "prefix": prefix})

        # for l in asn_leafs[a["asn"]]:
        #     pl = calc_posi(l[0], x_list, x_width)
        #     dots.append({"xp": "%.1f" % pl, "yp": thigh - 1.5, "color": dark_color, "other": l[1], "lgt": "%.1f" % l[0]})

    # # print(rects, dots)
    # thigh += 30

    for line in tier2_asns:
        high = 12
        for asn in line:
            a = {
                "asn": int(asn["asn"]),
                "yp": thigh + 1,
                "height": high,
                "name": "%s, %s, %s" % (asn["asn"], asn["name"], asn["country"]),  # f'{asn["asn"]}, {asn["name"]}, {asn["country"]}',
                "scale": asn["scale"],
                "color": asn["color"]
            }
            # a["color"], dark_color = rand_color()
            dark_color = asn["dark_color"]
            # print(len(asn["rects"]))
            b = {x: y for x, y in a.items()}
            b["xp"] = calc_posi(asn["rect"][0], x_list, x_width)
            b["width"] = calc_posi(asn["rect"][-1], x_list, x_width) - b["xp"]
            tier2_rects.append(b)

            prefixs = sorted(asn["prefixs"], key=lambda x: float(x[0]))
            for c in prefixs:
                prefix = " "
                leng = math.log2(float(c[1]))
                leng = leng if leng <= 24 else 24
                r = (high / 2 - 4) / 26 * leng + 2
                try:
                    pl = calc_posi(float(c[0]), x_list, x_width)
                except Exception as e:
                    print(c[0])
                    continue

                circles.append({"xp": "%.1f" % pl, "yp": thigh + high / 2, "r": "%.2f" %
                                r, "asn": int(asn["asn"]), "len": str(24 - leng)[:4], "color": dark_color, "prefix": prefix})

            # lgts = asn["rect"]
            # for l in lgts:
            #     lgtss.append({"xp": calc_posi(l, x_list, x_width), "yp": a["yp"], "width": 2,
            #                   "color": dark_color, "height": a["height"] - 3, "lgt": l})
            # for l in asn["dots"]:
            #     pl = calc_posi(l[0], x_list, x_width)
            #     dots.append(
            #         {"xp": "%.1f" % pl, "yp": thigh + 12, "color": dark_color, "other": l[1], "lgt": "%.1f" % l[0]})

            if asn["max"]:
                for x in asn["little"]:  # 画同自治域的小矩形
                    b = {x: y for x, y in a.items()}
                    b["xp"] = calc_posi(x - 2, x_list, x_width)
                    b["width"] = calc_posi(x + 2, x_list, x_width) - b["xp"]   # 小矩形宽4
                    tier2_rects.append(b)

        thigh += high
        nnn += 1
        if nnn % 5 == 0:
            yax_key.append(thigh - 50)
            yax_value.append(nnn)
    yax_key.append(thigh - 50)
    yax_value.append(nnn)

    # print(len(tier2_rects))
    return rects, lgtss, tier2_rects, circles, dots, yax_key, yax_value


arg = {"group": 85, "jiange": 50, "country_asn": {}, "results": ""}


def zipData(content):
    zbuf = BytesIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=zbuf)
    zfile.write(content.encode())
    zfile.close()
    return base64.b64encode(zbuf.getvalue())


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        # print(self.request.arguments)
        if "group" in self.request.arguments:
            arg["group"] = int(self.get_argument("group"))
        # else:
        #     arg["group"] = 85
        if "jiange" in self.request.arguments:
            arg["jiange"] = int(self.get_argument("jiange"))
        # else:
        #     arg["jiange"] = 50

        self.render("topo2.html")  # , x_list=x_list, x_domain=du_list, x_list2=x, x_domain2=du


class JsonHandler(tornado.web.RequestHandler):

    def get(self):
        if "group" in self.request.arguments:
            new_group = int(self.get_argument("group"))
        if "jiange" in self.request.arguments:
            new_jiange = int(self.get_argument("jiange"))

        if (new_group, new_jiange) == (arg["group"], arg["jiange"]) and arg["results"]:
            self.write(arg["results"])
            return
        else:
            arg["group"], arg["jiange"] = new_group, new_jiange
            tier1_asns, tier2_asns, asn_leafs, x_scae, arg["country_asn"] = get_info(jiange=arg["jiange"], group=arg["group"])
            x_scae = [x ** 1.7 for x in x_scae]
            x_width = [x / sum(x_scae) * 1200 for x in x_scae]
            x_list = [100 + sum(x_width[:i]) for i in range(len(x_width) + 1)]

            rects, lgts, tier2_rects, circles, dots, yax_key, yax_value = rect_posi(tier1_asns, tier2_asns, asn_leafs, x_list, x_width)

            pos_to_name = {x_list[0]: "", x_list[-1]: ""}
            # for city in citys:
            #     posi = calc_posi(citys[city][0], x_list, x_width)
            #     pos_to_name[posi] = city
            #     lines.append({"xp": posi})
            # x = list(sorted(pos_to_name.keys()))

            # du = [pos_to_name[m] for m in x] "lgts": lgts,

            result = json.dumps({"rects": rects, "lgts": lgts, "lines": lines, "rect2s": tier2_rects, "circles": circles, "dots": dots,
                                 "yax": [yax_key, yax_value], "xax": [x_list, du_list]})  # , x, du
            arg["results"] = zipData(result)
            self.write(arg["results"])


class SearchHandler(tornado.web.RequestHandler):

    def get(self):
        if "ip" in self.request.arguments:
            ip = self.get_argument("ip")
            rnode = rtree.search_best(ip)
            self.write(json.dumps({"asn": rnode.data["asn"], "prefix": rnode.prefix}))


class RelationHandler(tornado.web.RequestHandler):

    def get(self):
        if "asn" in self.request.arguments:
            asn = int(self.get_argument("asn"))
            self.write(json.dumps(relationship.get(asn, "null")))


class CountryHandler(tornado.web.RequestHandler):

    def get(self):
        if "code" in self.request.arguments:
            code = self.get_argument("code")
            self.write(json.dumps(arg["country_asn"].get(code, "null")))


class OtherHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("")

    def post(self):
        self.write("")


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    application = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/json", JsonHandler),
            (r"/search", SearchHandler),
            (r"/relation", RelationHandler),
            (r"/country", CountryHandler),
            (r"^/.*$", OtherHandler),
            # (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "/home/auto/bgpsim/web"})
        ],
        debug=True,
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(application)
    # http_server.bind(65530)
    # http_server.start(0)
    http_server.listen(5679)
    tornado.ioloop.IOLoop.instance().start()
