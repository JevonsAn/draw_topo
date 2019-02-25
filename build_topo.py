from handle.sql_conn2 import Mysql
from info import get_relations  # , get_prefix_tree


def get_relations2():
    mysqlserver = Mysql()
    sql = "SELECT * FROM topo_data.relationship;"
    mysqlserver.exe(sql)
    links = []
    for row in mysqlserver.results():
        links.append(row)
    mysqlserver.closeSQL()
    return links


def get_asninfo():
    mysqlserver = Mysql()
    sql = "SELECT a.asn, a.asname, a.country, a.customer_num, a.degree  FROM topo_data.asinfo a;"
    mysqlserver.exe(sql)
    asns = {}
    # print(mysqlserver.results(), flush=True)
    for row in mysqlserver.results():
        asns[row[0]] = list(row[1:])
    mysqlserver.closeSQL()
    return asns


relations = get_relations()
link_list = get_relations2()
asn_infos = get_asninfo()


def build_dict(asn):
    links = []
    nodes = []
    asn_set = {}

    MAX_pointsnum = 500

    peers = relations.get(asn, [[], [], []])[0][:MAX_pointsnum]
    NUM_peers = len(peers)
    center_asn_info = asn_infos.get(asn, [None, None, 0, 0])
    for x in peers:
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nodes.append({"asn": x, "asname": info[0], "country": info[1], "degree": info[2], "tier": 0})
            links.append({"source": asn, "target": x, "relationship": "P2P", "value": min(info[3] + 1, 1 + center_asn_info[3])})

    provider_query = [(asn, None, 0)]
    customer_query = [(asn, None, 0)]

    while (provider_query):
        x, last, tier = provider_query.pop(0)
        if tier >= 3:
            break
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nodes.append({"asn": x, "asname": info[0], "country": info[1], "degree": info[3], "tier": tier})
            if last:
                links.append({"source": last, "target": x, "relationship": "C2P", "value": min(info[3] + 1, 1 + asn_infos.get(last, [None, None, 0, 0])[3])})
                asn_set[last] += 1
                asn_set[x] += 1
            if len(asn_set) >= (MAX_pointsnum - NUM_peers) / 2 + NUM_peers:
                break
        providers = relations.get(x, [[], [], []])[1]
        provider_query.extend([(p, x, tier + 1) for p in providers])
        # for p in providers:
        #     links.append({"source": x, "target": p, "relationship": "C2P", "value": (info[3] + 1) * (1 + asn_infos.get(last, [None, None, 0, 0])[3] + 1)})

    while (customer_query):
        x, last, tier = customer_query.pop(0)
        if tier <= -3:
            break
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nodes.append({"asn": x, "asname": info[0], "country": info[1], "degree": info[3], "tier": tier})
            if last:
                links.append({"source": last, "target": x, "relationship": "P2C", "value": min(info[3] + 1, 1 + asn_infos.get(last, [None, None, 0, 0])[3])})
                asn_set[last] += 1
                asn_set[x] += 1
            if len(asn_set) >= MAX_pointsnum:
                break
        customers = relations.get(x, [[], [], []])[2]
        customer_query.extend([(p, x, tier - 1) for p in customers])
    for n in nodes:
        n["linknum"] = asn_set[n["asn"]]
    return {"nodes": nodes, "links": links}


def build_dict2(asn):
    links = []
    nodes = []
    asn_set = {}

    MAX_pointsnum = 500

    peers = relations.get(asn, [[], [], []])[0][:MAX_pointsnum]
    NUM_peers = len(peers)
    center_asn_info = asn_infos.get(asn, [None, None, 0, 0])
    for x in peers:
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nodes.append({"asn": x, "asname": info[0], "country": info[1], "degree": info[2], "tier": 0})

    provider_query = [(asn, 0)]
    customer_query = [(asn, 0)]
    while (provider_query):
        x, tier = provider_query.pop(0)
        if tier >= 3:
            break
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nodes.append({"asn": x, "asname": info[0], "country": info[1], "degree": info[3], "tier": tier})
            if len(asn_set) >= (MAX_pointsnum - NUM_peers) / 2 + NUM_peers:
                break
        providers = relations.get(x, [[], [], []])[1]
        provider_query.extend([(p, tier + 1) for p in providers])
        # for p in providers:
        #     links.append({"source": x, "target": p, "relationship": "C2P", "value": (info[3] + 1) * (1 + asn_infos.get(last, [None, None, 0, 0])[3] + 1)})

    while (customer_query):
        x, tier = customer_query.pop(0)
        if tier <= -3:
            break
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nodes.append({"asn": x, "asname": info[0], "country": info[1], "degree": info[3], "tier": tier})
            if len(asn_set) >= MAX_pointsnum:
                break
        customers = relations.get(x, [[], [], []])[2]
        customer_query.extend([(p, tier - 1) for p in customers])

    for link in link_list:
        if link[0] in asn_set and link[1] in asn_set:
            info1 = asn_infos.get(link[0], [None, None, 0, 0])
            info2 = asn_infos.get(link[1], [None, None, 0, 0])
            links.append({"source": link[0], "target": link[1], "relationship": link[2], "value": min(info1[3], info2[3])})
            asn_set[link[0]] += 1
            asn_set[link[1]] += 1
    for n in nodes:
        n["linknum"] = asn_set[n["asn"]]
    return {"nodes": nodes, "links": links}


def build_dict3(asn):
    cus_nodes = []
    pro_nodes = []
    asn_set = {}

    MAX_pointsnum = 100

    provider_query = [(asn, None, 0)]
    customer_query = [(asn, None, 0)]

    while (provider_query):
        x, last, tier = provider_query.pop(0)
        if tier >= 3:
            break
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nd = {"asn": x, "name": x, "asname": info[0], "country": info[1], "degree": info[3], "tier": tier}
            if last:
                nd["parent"] = last
                asn_set[last] += 1
                asn_set[x] += 1
            else:
                nd["parent"] = ""
            pro_nodes.append(nd)
            if len(asn_set) >= MAX_pointsnum:
                break

        providers = relations.get(x, [[], [], []])[1]
        provider_query.extend([(p, x, tier + 1) for p in providers])
    for n in pro_nodes:
        n["linknum"] = asn_set[n["asn"]]

    asn_set = {}

    while (customer_query):
        x, last, tier = customer_query.pop(0)
        if tier <= -3:
            break
        if x not in asn_set:
            asn_set[x] = 0
            info = asn_infos.get(x, [None, None, 0, 0])
            nd = {"asn": x, "name": x, "asname": info[0], "country": info[1], "degree": info[3], "tier": tier}
            if last:
                nd["parent"] = last
                asn_set[last] += 1
                asn_set[x] += 1
            else:
                nd["parent"] = ""
            cus_nodes.append(nd)
            if len(asn_set) >= MAX_pointsnum:
                break
        customers = relations.get(x, [[], [], []])[2]
        customer_query.extend([(p, x, tier - 1) for p in customers])

    for n in cus_nodes:
        n["linknum"] = asn_set[n["asn"]]

    return {"customers": cus_nodes, "providers": pro_nodes}


if __name__ == '__main__':
    d = build_dict(34478)
    print(relations[34478])
    print(len(d["nodes"]), len(d["links"]))
    # print(d["nodes"])
