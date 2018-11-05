import math
import random
import datetime
# import json

citys = {
    "北京": [116.39723, 39.9075],
    "纽约": [
        -75.29128,
        43.10535
    ],
    "洛杉矶": [
        -118.15,
        34.04
    ],
    "夏威夷": [
        -155.33,
        19.46
    ],
    "伦敦": [
        0.10,
        51.30
    ],
    "莫斯科": [
        37.35,
        55.45
    ],
    "新德里": [
        77.13,
        28.37

    ],
    "东京": [
        139.46,
        35.42
    ],
    "旧金山": [
        -122.25,
        37.46
    ],
    "西雅图": [
        -122.19,
        47.36
    ],
    "圣保罗": [
        -46.38,
        -23.33
    ],
    "新加坡": [
        103.45,
        1.22
    ],
    "上海": [
        121.27,
        31.14
    ],
    "悉尼": [
        151.17,
        -33.55
    ],
    "丹佛": [
        -104.59,
        39.43
    ],
    "芝加哥": [
        -87,
        41.51
    ],
    "阿姆斯特丹": [
        4.52,
        52.21
    ],
    "华沙": [
        21,
        52.15
    ],
    "柏林": [
        13.2,
        52.31
    ],
    "香港": [
        114,
        22.17
    ],
    "休斯顿": [
        -95.23,
        29.6
    ],
    "多伦多": [
        -79.33,
        43.6
    ],
    "波士顿": [
        -71,
        42.29
    ],
    "盐湖城": [
        -111.89,
        40.7
    ],
    "孟买": [
        72.8,
        18.95
    ],


}

p_list = [-180, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]


def rand_color():
    def hsv2rgb(h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    h = random.randint(0, 360)
    s = random.randint(0, 150) / 256
    v = 200 / 256
    r, g, b = hsv2rgb(h, s, v)
    # print(h,s,v)
    res = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res = res.upper().replace(" ", "0")

    h = random.randint(h - 20, h + 20)
    s = random.randint(int(s * 256 - 20), int(s * 256 + 20)) / 256
    v = 150 / 256

    r, g, b = hsv2rgb(h, s, v)
    # print(h,s,v)
    res2 = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res2 = res2.upper().replace(" ", "0")
    return res, res2


def rand_color2(color):
    def hsv2rgb(h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    def rgb2hsv(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v

    def randinter(sv, rg):
        inter1 = [sv - rg, sv + rg]
        if inter1[0] < 0:
            inter1[0] = 0
        if inter1[1] > 1:
            inter1[1] = 1
        s1 = random.random() * (inter1[1] - inter1[0]) + inter1[0]
        return s1

    def randh(sv, rg):
        inter1 = [sv - rg, sv + rg]
        if inter1[0] < 0:
            inter1[0] = 0
        if inter1[1] > 255:
            inter1[1] = 255
        s1 = random.random() * (inter1[1] - inter1[0]) + inter1[0]
        return s1

    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    h, s, v = rgb2hsv(r, g, b)
    h1, s1, v1 = randh(h, 15), randinter(s, 0.25), randinter(v, 0.25)
    # print(h1, s1, v1)
    r, g, b = hsv2rgb(h1, s1, v1)
    res = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res = res.upper().replace(" ", "0")
    # print(res)

    h2 = random.randint(int(h1 - 20), int(h1 + 20))
    s2 = random.randint(int(s1 * 256 - 20), int(s1 * 256 + 20)) / 256
    v2 = (v1 * 256 - 50) / 256

    r, g, b = hsv2rgb(h2, s2, v2)
    res2 = "#%2s" % hex(r)[2:] + "%2s" % hex(g)[2:] + "%2s" % hex(b)[2:]
    res2 = res2.upper().replace(" ", "0")
    return res, res2


def calc_width(l, jiange):
    max_wid = 0
    max_index = 0
    for i in range(len(l) - 1):
        this = l[i]
        next = l[i + 1]
        wid = next - this
        if wid > max_wid:
            max_wid = wid
            max_index = i + 1
    this = l[len(l) - 1]
    next = l[0]
    # if this * next < 0:
    wid = 180 - this + next + 180
    if wid > max_wid:
        max_wid = wid
        max_index = 0
    indexs = []
    indexs.append(max_index)
    for i in range(0, len(l) - 1):
        ai = (max_index + i) % len(l)
        bi = (max_index + i + 1) % len(l)
        this = l[ai]
        next = l[bi]
        if bi == 0:
            wid = 180 - this + next + 180
        else:
            wid = next - this
        if wid > jiange:
            indexs.append(bi)

    rects = [(l[x], l[(indexs[i + 1]) - 1]) for i, x in enumerate(indexs[:-1])] + [(l[indexs[-1]], l[indexs[0] - 1],)]  # % len(l)
    new_rects = []
    for i, r in enumerate(rects):
        if r[0] == r[1]:
            # new_rects.append((r[0] - 3, r[0] + 3))
            new_rects.append((r[0], r[0] + 4))
        elif r[0] > r[1]:
            new_rects.append((r[0], 180))
            new_rects.append((-180, r[1]))
        else:
            new_rects.append(r)
    return new_rects


def calc_width22(l, jiange, leafs):
    # 寻找差别最大点作为起点
    max_wid = 0
    max_index = 0
    for i in range(len(l) - 1):
        this = l[i]
        next = l[i + 1]
        wid = next - this
        if wid > max_wid:
            max_wid = wid
            max_index = i + 1
    this = l[len(l) - 1]
    next = l[0]
    # if this * next < 0:
    wid = 180 - this + next + 180
    if wid > max_wid:
        max_wid = wid
        max_index = 0
    # print(l, max_index, max_wid)

    # 根据间隔分成小区间
    rects = []
    sub = [l[max_index]]
    for i in range(0, len(l) - 1):
        ai = (max_index + i) % len(l)
        bi = (max_index + i + 1) % len(l)
        this = l[ai]
        next = l[bi]
        if bi == 0:
            wid = 180 - this + next + 180
        else:
            wid = next - this
        if wid > jiange:
            rects.append(sub)
            sub = [l[bi]]
        else:
            sub.append(l[bi])
    rects.append(sub)
    # print(rects)

    # 整理最大区间、筛出小区间
    new_rects = []
    little = []
    max_len = 1
    max_index = 0
    for i, r in enumerate(rects):
        if len(r) == 1:
            # new_rects.append((r[0] - 3, r[0] + 3))
            little.append(r[0])
        elif r[0] > r[-1]:
            positive = []
            negative = [-180]
            for x in r:
                if x >= 0:
                    positive.append(x)
                else:
                    negative.append(x)
            positive.append(180)
            new_rects.append({"rect": positive, "max": False, "dots": []})
            if len(positive) > max_len:
                max_len = len(positive)
                max_index = len(new_rects) - 1
            new_rects.append({"rect": negative, "max": False, "dots": []})
            if len(negative) > max_len:
                max_len = len(negative)
                max_index = len(new_rects) - 1
        else:
            new_rects.append({"rect": r, "max": False, "dots": []})
            if len(r) > max_len:
                max_len = len(r)
                max_index = len(new_rects) - 1

    new_rects.sort(key=lambda x: x["rect"])
    leafs.sort(key=lambda x: x[0])
    if len(new_rects) == 0:
        new_rects.append({"rect": [0, 0], "max": False, "dots": leafs})
    elif len(new_rects) == 1:
        new_rects[0]["dots"] = leafs
    else:
        now_index = 0
        for leafset in leafs:
            if now_index + 1 >= len(new_rects):
                new_rects[now_index]["dots"].append(leafset)
                continue

            leaf = int(leafset[0])
            left_end = new_rects[now_index]["rect"][-1]
            right_start = new_rects[now_index + 1]["rect"][0]

            if leaf <= left_end:
                new_rects[now_index]["dots"].append(leafset)
            elif leaf >= right_start:
                while True:
                    if leaf >= new_rects[now_index + 1]["rect"][0]:
                        now_index += 1
                        if now_index + 1 >= len(new_rects):
                            break
                    else:
                        break
                if now_index >= len(new_rects):
                    new_rects[-1]["dots"].append(leafset)
                else:
                    new_rects[now_index]["dots"].append(leafset)
            else:
                if leaf - left_end < right_start - leaf:
                    new_rects[now_index]["dots"].append(leafset)
                else:
                    new_rects[now_index + 1]["dots"].append(leafset)
                    now_index += 1
        new_rects[max_index]["max"] = True
        new_rects[max_index]["little"] = little
    # print(new_rects)
    return new_rects


def Interval_Merge(itv_list, group):
    result_list = []
    sub_list = [sorted(itv_list[x: x + group], key=lambda As: As['rect']) for x in range(0, len(itv_list), group)]
    # print(sub_list)
    for l in sub_list:
        slist = []
        lset = [1] * len(l)
        for i, x in enumerate(l):
            for j, y in enumerate(l[i:]):
                if lset[i + j]:
                    if not slist or slist[-1]['rect'][-1] <= y['rect'][0]:
                        slist.append(y)
                        lset[i + j] = 0
            if slist:
                result_list.append(slist)
            slist = []
    return result_list


country_color = {
    "US": "#87CEEB",
    "BR": "#008000",
    "RU": "#FFFF00",
    "PL": "#9400D3",
    "GB": "#FFC0CB",
    "UA": "#DAA520",
    "DE": "#808080",
    "NL": "#0000FF",
    "CA": "#B22222",
    "FR": "#90EE90",
    "IN": "#FF8C00",
    "HK": "#FF0000",
    "CN": "#FF0000",
    "JP": "#D3D3D3",
}


def get_info(jiange=50, group=85):   # jiange = 50 空白多少用来分割大矩形
    x_scale = [0] * (len(p_list) - 1)

    def calc_posi(rects):
        # print(rects)
        for rx in rects:
            # print(rx)
            t0 = len(p_list) - 2
            for i in range(len(p_list) - 1):
                if p_list[i] <= rx[0] < p_list[i + 1]:
                    t0 = i
                    break
            t1 = len(p_list) - 2
            for i in range(len(p_list) - 1):
                if p_list[i] <= rx[1] < p_list[i + 1]:
                    t1 = i
                    break
            if t1 > t0:
                x_scale[t0] += p_list[t0 + 1] - rx[0]
                x_scale[t1] += rx[1] - p_list[t1]
                for t in range(t0 + 1, t1):
                    x_scale[t] += p_list[t + 1] - p_list[t]
            else:
                x_scale[t0] += rx[1] - rx[0]

    asn_leafs = dict()
    # 262589|265315|BINDNET RJ|BR|-43.0|-22.9028|(262589, 262788, 265315)|['168.121.176.0/24', '168.121.177.0/24', '168.121.178.0/24', '168.121.179.0/24']
    with open("static/leafs.txt", encoding="utf-8") as f:
        for line in f.readlines():
            sp = line.strip().split("|")
            pvd = int(sp[0])
            lgt = float(sp[4])
            other = f'{sp[1]}|{sp[2]}|{sp[3]}|{sp[5]}|{sp[6]}|{sp[7]}'
            if pvd not in asn_leafs:
                asn_leafs[pvd] = [(lgt, other)]
            else:
                asn_leafs[pvd].append((lgt, other))

    tier1_asns = []
    with open("static/tier1_info.txt") as f:
        for line in f.readlines():
            sp = line.strip().split("|")
            As = {}
            if len(sp) == 7:
                As["asn"], As["name"], As["country"], As["scale"], As["posis"], As["dms"] = sp[:-1]
                As["posis"] = eval(As["posis"])
                As["rects"] = calc_width(As["posis"], jiange)
                if As["country"] not in country_color:
                    As["color"], As["dark_color"] = rand_color()
                else:
                    As["color"], As["dark_color"] = rand_color2(country_color[As["country"]])
                tier1_asns.append(As)
                calc_posi(As["rects"])
                # if As["country"] not in country_count:
                #     country_count[As["country"]] = 1
                # else:
                #     country_count[As["country"]] += 1

    tier2_asns = []
    with open("static/tier2_info.txt") as f:
        for line in f.readlines():
            sp = line.strip().split("|")
            if len(sp) == 7:
                As = {}
                As["asn"], As["name"], As["country"], As["scale"], As["posis"], As["dms"] = sp[:-1]
                As["posis"] = eval(As["posis"])
                if As["country"] not in country_color:
                    As["color"], As["dark_color"] = rand_color()
                else:
                    As["color"], As["dark_color"] = rand_color2(country_color[As["country"]])
                # if As["country"] not in country_count:
                #     country_count[As["country"]] = 1
                # else:
                #     country_count[As["country"]] += 1
                rects = calc_width22(As["posis"], jiange, asn_leafs.get(int(As["asn"]), []))  # 在这里把矩形分成小矩形 As["posis"], jiange
                # print(rects)
                for rx in rects:
                    b = {x: y for x, y in As.items() if x != "posis"}
                    b.update(rx)
                    tier2_asns.append(b)
                calc_posi([(x["rect"][0], x["rect"][-1]) for x in rects])

    tier2_asns = Interval_Merge(tier2_asns, group)
    return tier1_asns, tier2_asns, asn_leafs, x_scale


def get_relations():
    relation_text = ""
    with open("static/get_relations.txt") as f:
        relation_text = f.read()
    relations = eval(relation_text)
    return relations
