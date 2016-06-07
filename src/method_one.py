from src.tool import get_time_links

"""
    Find how many nodes can access the node identified by vertex_id
    before time.
"""
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
    return compute_dist_node(l, 0, nb_v)


def compute_dist(timelink_list, nb_vertexes):
    prev_time = -1
    cur_time = -1;

    mat = [[0]*nb_vertexes for i in range(nb_vertexes)]
    mat_prev = [[0]*nb_vertexes for i in range(nb_vertexes)]
    result = []

    # Matrix initialisation
    for i in range(nb_vertexes):
        for j in range(nb_vertexes):
            mat[i][j] = -1
            mat_prev[i][j] = -1
        mat_prev[i][i] = 0

    for elem in timelink_list:
        if cur_time == -1:
            prev_time = elem.time
            cur_time = elem.time
            for i in range(nb_vertexes):
                mat[i][i] = cur_time

        prev_time = cur_time
        cur_time = elem.time

        if prev_time != cur_time:
            for i in range(nb_vertexes):
                for j in range(nb_vertexes):
                    mat_prev[i][j] = mat[i][j]
                mat[i][i] = cur_time

        mat[elem.nodeA][elem.nodeB] = cur_time
        mat[elem.nodeB][elem.nodeA] = cur_time

        for i in range(nb_vertexes):
            if (i != elem.nodeA) and (i != elem.nodeB):
                if mat_prev[elem.nodeA][i] != -1:
                    if mat_prev[elem.nodeB][i] != -1:
                        if mat[elem.nodeA][i] > mat_prev[elem.nodeB][i]:
                            mat[elem.nodeA][i] = mat_prev[elem.nodeB][i]
                        elif mat[elem.nodeB][i] > mat_prev[elem.nodeA][i]:
                            mat[elem.nodeB][i] = mat_prev[elem.nodeA][i]
                    else:
                        if mat[elem.nodeB][i] == -1 or mat[elem.nodeB][i] > mat_prev[elem.nodeA][i]:
                            mat[elem.nodeB][i] = mat_prev[elem.nodeA][i]
                else:
                    if mat_prev[elem.nodeB][i] != -1:
                        if mat[elem.nodeA][i] == -1 or mat[elem.nodeA][i] > mat_prev[elem.nodeB][i]:
                            mat[elem.nodeA][i] = mat_prev[elem.nodeB][i]

    for i in range(nb_vertexes):
        mat[i][i] = cur_time

    nb_in = 0
    nb_out = 0
    for i in range(nb_vertexes):
        for j in range(nb_vertexes):
            if mat[i][j] != -1 and i != j:
                nb_out += 1
            if mat[j][i] != -1 and i != j:
                nb_in += 1
        result.append({i: (nb_in, nb_out)})
        nb_in = 0
        nb_out = 0

    # Debug logs only when its human readable
    if nb_vertexes < 10:
        for i in range(nb_vertexes):
            print mat[i]

    compute_dist_node(timelink_list, 1, nb_vertexes)

    return result


def compute_dist_node(timelink_list, vertex_id, nb_vertexes):

    res = [-1 for i in range(nb_vertexes)]
    res_prev = [-1 for i in range(nb_vertexes)]
    cur_time = -1
    res[vertex_id] = 0

    for elem in timelink_list:
        res[vertex_id] = elem.time

        if elem.nodeA == vertex_id:
            cur_time = elem.time
            res[elem.nodeB] = cur_time
        elif elem.nodeB == vertex_id:
            cur_time = elem.time
            res[elem.nodeA] = cur_time

        prev_time = cur_time
        cur_time = elem.time

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
                if res[elem.nodeB] == -1 or res[elem.nodeB] > res[elem.nodeA]:
                    res[elem.nodeB] = res_prev[elem.nodeA]
        else:
            if res_prev[elem.nodeB] != -1:
                if res[elem.nodeA] == -1 or res[elem.nodeA] > res_prev[elem.nodeB]:
                    res[elem.nodeA] = res_prev[elem.nodeB]

    nb_out = 0
    for i in range(nb_vertexes):
        if res[i] != -1 and i != vertex_id:
            nb_out += 1
    print "nb_in[" + str(vertex_id) + "] = " + str(nb_out)

    print res

    return res

"""
    Finds how many nodes can access the one identified by vertex_id
    @:return array of ids (size: nb_vertexes)
"""
def compute_nb_in(timelink_list, vertex_id, nb_vertexes):
    res = [-1 for i in range(nb_vertexes)]
    res_prev = [-1 for i in range(nb_vertexes)]
    cur_time = -1
    res[vertex_id] = 0

    for elem in timelink_list:
        res[vertex_id] = elem.time

    return res
