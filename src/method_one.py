from src.tool import get_time_links

"""
    Check if there is a temporal path between u and v starting on 0 (or after) and
    arriving before t.
    @:return true or false
"""
def check_path(mat, visited, u, v, t):

    return False


def adjacent(graph, start):
    return graph.get(start)


"""
    Recursive version of the DFS for timelinked graphs
"""
def recursive_dfs(graph, start, path=set()):
    visited = {}
    nb_visited = 0

    # for e in vertexes:
    #    visited.update({e: False})

    adj = adjacent(graph, start)

    while nb_visited != len(adj):
        for i in range(len(adj)):
            print i


def dfs(graph, start):
    visited, stack = [], [start]
    last_time = 0

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            l = graph.get(vertex)
            if l[0].time > last_time:
                visited.append(vertex)
                tmp = [l[0].nodeA, l[0].nodeB]
                stack.extend(tmp)

            # print graph.get(vertex)
            # visited.append(vertex)
            # stack.extend(graph[vertex] - visited)

    return visited


def iterative_dfs(graph, start, path=[]):

    q = [start]
    print str(graph.get(start)[0])
    # last = start.time

    print graph.get(start)

    while q:
        v = q.pop(0)
        if v not in path:
            path = path + [v]
            # q = graph[v] + q
    return path


"""
    Find how many nodes can access the node identified by vertex_id
    before time.
"""
def algo(filename, vertex_id, time):

    nb_in = 0
    mat = {}
    (l, vertexes) = get_time_links(filename)
    elems = filter(lambda e: e.time < time, l)
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
    return compute_dist(l, nb_v, vertex_id)


def compute_dist(l, nb_vertexes, vertex_id):
    # print "> " + str(vertexes) + " nbv: " + str(nb_v)

    prev_time = -1
    cur_time = -1;

    mat = [[0]*nb_vertexes for i in range(nb_vertexes)]
    mat_prev = [[0]*nb_vertexes for i in range(nb_vertexes)]

    # Matrix intialisation
    for i in range(nb_vertexes):
        for j in range(nb_vertexes):
            mat[i][j] = -1
            mat_prev[i][j] = -1
        mat_prev[i][i] = 0

    for elem in l:
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
        if mat[vertex_id][i] != -1 and i != vertex_id:
            nb_in += 1
        if mat[i][vertex_id] != -1 and i != vertex_id:
            nb_out += 1
    # for i in range((nb_vertexes)):
    #    print mat[i]
    # print "nb_in: " + str(nb_in) + " nb_out: " + str(nb_out)

    return (nb_in, nb_out)

