import math
import random

jiange = 50  # 空白多少用来分割大矩形


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


def calc_width22(l, jiange):
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
            new_rects.append({"rect": positive, "max": False})
            if len(positive) > max_len:
                max_len = len(positive)
                max_index = len(new_rects) - 1
            new_rects.append({"rect": negative, "max": False})
            if len(negative) > max_len:
                max_len = len(negative)
                max_index = len(new_rects) - 1
        else:
            new_rects.append({"rect": r, "max": False})
            if len(r) > max_len:
                max_len = len(r)
                max_index = len(new_rects) - 1
    # print(new_rects, max_index, max_len)
    if len(new_rects) == 0:
        new_rects.append({"rect": [0, 0], "max": False})
    new_rects[max_index]["max"] = True
    new_rects[max_index]["little"] = little
    return new_rects


asn_leafs = dict()
# 18881|22561|RPNET INFORMATICA LTDA - ME|BR|-53.4552996887207|-24.9558
with open("static/leafs.txt", encoding="utf-8") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        pvd = int(sp[0])
        lgt = float(sp[4])
        other = f'{sp[1]}|{sp[2]}|{sp[3]}|{sp[5]}|{sp[6]}'
        if pvd not in asn_leafs:
            asn_leafs[pvd] = [(lgt, other)]
        else:
            asn_leafs[pvd].append((lgt, other))


tier1_asns = []
with open("static/tier1_info.txt") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        As = {}
        if len(sp) == 6:
            As["asn"], As["name"], As["country"], As["scale"], As["posis"], As["dms"] = sp
            As["posis"] = eval(As["posis"])
            As["rects"] = calc_width(As["posis"], jiange)
            tier1_asns.append(As)


tier2_asns = []
with open("static/tier2_info.txt") as f:
    for line in f.readlines():
        sp = line.strip().split("|")
        if len(sp) == 6:
            As = {}
            As["asn"], As["name"], As["country"], As["scale"], As["posis"], As["dms"] = sp
            As["posis"] = eval(As["posis"])
            As["color"], As["dark_color"] = rand_color()

            # print(As)
            rects = calc_width22(As["posis"],  50)  # 在这里把矩形分成小矩形 As["posis"], jiange

            # rects变了，此处要修改

            for rx in rects:
                b = {x: y for x, y in As.items() if x != "posis"}
                b.update(rx)
                tier2_asns.append(b)
# for line in tier2_asns:
#     print([y["lgt"] for y in line])

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
