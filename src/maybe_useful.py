from src.tool import get_time_links


def algo(filename, time):

    nb_in = 0
    mat = {}
    (l, vertexes) = get_time_links(filename)
    # elems = filter(lambda e: e.time < time, l)
    # elems.sort(key=lambda e: e.time)

    # Foreach node list its neighbours
    # Map<Node, [neighbours]>
    # for elem in elems:
    #    try:
    #        mat[str(elem.nodeA)].append(elem)
    #    except KeyError:
    #        mat[str(elem.nodeA)] = [elem]
    #    try:
    #        mat[str(elem.nodeB)].append(elem)
    #    except KeyError:
    #        mat[str(elem.nodeB)] = [elem]

    # print "\n========== Nodes ==========\n"
    # print vertexes
    # print "\n---------------------------\n"

    # for k, v in mat.items():
    #    print k + " [" + ', '.join(map(str, v)) + "]"
    # tmp_mat = None

    # for k in mat:
    #    print k
    #    tmp_mat = copy.deepcopy(mat) # EVIL !!!
    #    if check_path(tmp_mat, [], int(k), vertex_id, time):
    #        nb_in += 1

    # print "Nombre de in : " + str(nb_in) + " du sommet : " + str(vertex_id)
    # tmp_mat["1"] = []
    # for k, v in mat.items():
    #    print k + " [" + ', '.join(map(str, v)) + "]"

    # print "-------------"
    # for k, v in tmp_mat.items():
    #    print k + " [" + ', '.join(map(str, v)) + "]"

    # graph = { 1: set([2, 3]), 2: set([1]), 3: set([1, 2]) }
    # print graph
    # print iterative_dfs(tmp_mat, "1")
    # print recursive_dfs(tmp_mat, "1")
    # print dfs(mat, "1")
    nb_v = len(vertexes)
    # return compute_dist(l, nb_v)
    return []


def compute_vertex_nb_out_opt(links, nb_vertexes, vertex_id):
    if len(links) <= 0:
        raise Exception("Helppppppp! links is empty!")

    res = [-1 for _ in range(nb_vertexes)]
    res_prev = [-1 for _ in range(nb_vertexes)]
    cur_time = -1
    res[vertex_id] = 0
    links.sort(key=lambda e: e.time)
    res[vertex_id] = links[0].time

    for elem in links:

        if cur_time == -1:
            cur_time = elem.time

        prev_time = cur_time
        cur_time = elem.time

        if elem.nodeA == vertex_id:
            res[elem.nodeB] = cur_time
        elif elem.nodeB == vertex_id:
            res[elem.nodeA] = cur_time

        if prev_time != cur_time:
            for i in range(nb_vertexes):
                res_prev[i] = res[i]

        if res_prev[elem.nodeA] != -1:
            if res_prev[elem.nodeB] != -1:
                if res[elem.nodeA] > res[elem.nodeB]:
                    res[elem.nodeA] = res[elem.nodeB]
                elif res[elem.nodeB] > res[elem.nodeA]:
                    res[elem.nodeB] = res[elem.nodeA]
            else:
                if res[elem.nodeB] == -1:
                    res[elem.nodeB] = cur_time
                elif res[elem.nodeB] > res[elem.nodeA]:
                    # res[elem.nodeB] = cur_time  # res_prev[elem.nodeA]
                    print res_prev
                    print res
                    # print "Je m'attendais vertex_id:" + str(vertex_id) + " node: " + str(elem.nodeB) + " cur_time: " \
                    #      + str(cur_time) + " val: " + str(res_prev[elem.nodeB])
        else:
            if res_prev[elem.nodeB] != -1:
                if res[elem.nodeA] == -1:
                    res[elem.nodeA] = cur_time
                elif res[elem.nodeA] > res_prev[elem.nodeB]:
                    res[elem.nodeA] = cur_time  # res_prev[elem.nodeB]

    nb_out = 0
    for i in range(nb_vertexes):
        if res[i] != -1 and i != vertex_id:
            nb_out += 1

    # print res

    return nb_out, res
