from src.tool import get_time_links
import copy

"""
    Check if there is a temporal path between u and v starting on 0 (or after) and
    arriving before t.
    @:return true or false
"""
def check_path(mat, visited, u, v, t):

    return False

def iterative_dfs(graph, start, path=[]):

    q = [start]

    while q:
        v = q.pop(0)
        if v not in path:
            path = path + [v]
            q = graph[v] + q
    return path

"""
    Find how many nodes can access the node identified by vertex_id
    before time.
"""
def algo(filename, vertex_id, time):

    nb_in = 0;
    mat   = {}
    elems = filter(lambda e: e.time < time, get_time_links(filename))
    elems.sort(key=lambda e: e.time)

    # Foreach node list its neighbours
    # Map<Node, [neighbours]>
    for elem in elems:
        try:
            mat[str(elem.nodeA)].append(elem)
        except KeyError:
            mat[str(elem.nodeA)] = [ elem ]
        try:
            mat[str(elem.nodeB)].append(elem)
        except KeyError:
            mat[str(elem.nodeB)] = [elem]

    # for k, v in mat.items():
    #    print k + " [" + ', '.join(map(str, v)) + "]"
    tmp_mat = None

    for k in mat:
        print k
        tmp_mat = copy.deepcopy(mat)
        if check_path(tmp_mat, [], int(k), vertex_id, time):
            nb_in += 1

    print "Nombre de in : " + str(nb_in) + " du sommet : " + str(vertex_id)
    tmp_mat["1"] = []
    for k, v in mat.items():
        print k + " [" + ', '.join(map(str, v)) + "]"

    print "-------------"
    for k, v in tmp_mat.items():
        print k + " [" + ', '.join(map(str, v)) + "]"

    print "\n$$$$$$$$$$$$$\n"

    graph = { 1: [2, 3], 2: [1], 3: [1, 2] }
    print iterative_dfs(graph, 1)