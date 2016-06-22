def compute_nb_in_out(links, nb_vertexes):
    if len(links) <= 0:
        raise Exception("Help! links is empty!")

    cur_time = -1
    mat = [[0]*nb_vertexes for _ in range(nb_vertexes)]
    mat_prev = [[0]*nb_vertexes for _ in range(nb_vertexes)]
    result = []

    for i in range(nb_vertexes):
        for j in range(nb_vertexes):
            mat[i][j] = -1
            mat_prev[i][j] = -1
        mat_prev[i][i] = 0

    for elem in links:
        if cur_time == -1:
            cur_time = elem.time
            for i in range(nb_vertexes):
                mat[i][i] = cur_time

        prev_time = cur_time
        cur_time = elem.time

        if prev_time != cur_time:
            # for i in range(nb_vertexes):
            #    for j in range(nb_vertexes):
            #        mat_prev[i][j] = mat[i][j]
            #    mat[i][i] = cur_time

            # This one is slightly faster
            for i in range(nb_vertexes):
                mat[i][i] = cur_time
            mat_prev = [row[:] for row in mat]

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

    # Debug logs only when it's human readable
    if nb_vertexes < 10:
        for i in range(nb_vertexes):
            print mat[i]
        print

    return result


def compute_nb_in_out_array(links, nb_vertexes):
    res_nb_out = [0 for _ in range(nb_vertexes)]
    res_nb_in = [0 for _ in range(nb_vertexes)]
    result = []

    for i in range(nb_vertexes):
        tmp = compute_vertex_nb_in(links, nb_vertexes, i)

        for j in range(nb_vertexes):
            if j != i and tmp[1][j] != -1:
                res_nb_out[j] += 1
        res_nb_in[i] = tmp[0]

    for i in range(nb_vertexes):
        result.append({i: (res_nb_in[i], res_nb_out[i])})

    return result


def compute_vertex_nb_in(links, nb_vertexes, vertex_id):
    if len(links) <= 0:
        raise Exception("Help! links is empty!")

    res = [-1 for _ in range(nb_vertexes)]
    res_prev = [-1 for _ in range(nb_vertexes)]
    cur_time = -1
    res[vertex_id] = 0
    i_prev = -1

    for elem in links:
        res[vertex_id] = elem.time

        if elem.nodeA == vertex_id:
            cur_time = elem.time
            res[elem.nodeB] = cur_time
            i_prev = elem.nodeB
        elif elem.nodeB == vertex_id:
            cur_time = elem.time
            res[elem.nodeA] = cur_time
            i_prev = elem.nodeA

        prev_time = cur_time
        cur_time = elem.time

        if prev_time != cur_time:
            if i_prev != -1:
                res_prev[i_prev] = res[i_prev]

        #    for i in range(nb_vertexes):
        #        res_prev[i] = res[i]

        if res_prev[elem.nodeA] != -1:
            if res_prev[elem.nodeB] != -1:
                if res[elem.nodeA] > res[elem.nodeB]:
                    res[elem.nodeA] = res[elem.nodeB]
                    i_prev = elem.nodeA
                elif res[elem.nodeB] > res[elem.nodeA]:
                    res[elem.nodeB] = res[elem.nodeA]
                    i_prev = elem.nodeB
            else:
                if res[elem.nodeB] == -1 or res[elem.nodeB] > res[elem.nodeA]:
                    res[elem.nodeB] = res_prev[elem.nodeA]
                    i_prev = elem.nodeB
        else:
            if res_prev[elem.nodeB] != -1:
                if res[elem.nodeA] == -1 or res[elem.nodeA] > res_prev[elem.nodeB]:
                    res[elem.nodeA] = res_prev[elem.nodeB]
                    i_prev = elem.nodeA

    nb_in = 0
    for i in range(nb_vertexes):
        if res[i] != -1 and i != vertex_id:
            nb_in += 1

    return nb_in, res


def compute_vertex_nb_in2(links, nb_vertexes, vertex_id):
    if len(links) <= 0:
        raise Exception("Help! links is empty!")

    res = [-1 for _ in range(nb_vertexes)]
    res_prev = [-1 for _ in range(nb_vertexes)]
    cur_time = -1
    res[vertex_id] = 0

    for elem in links:
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

    nb_in = 0
    for i in range(nb_vertexes):
        if res[i] != -1 and i != vertex_id:
            nb_in += 1

    return nb_in, res


def compute_vertex_nb_out(links, nb_vertexes, vertex_id):
    if len(links) <= 0:
        raise Exception("Help! links is empty!")

    nb_out = 0
    res = [-1 for _ in range(nb_vertexes)]

    res[vertex_id] = vertex_id
    for i in range(nb_vertexes):
        if i != vertex_id:
            result = compute_vertex_nb_in(links, nb_vertexes, i)
            if result[1][vertex_id] != -1:
                nb_out += 1
                res[i] = result[1][vertex_id]

    return nb_out, res


def nb_in_out_with_fixed_value(result, value):
    nb = 0

    for i in range(len(result)):
        if result[i].get(i)[0] == value or result[i].get(i)[1] == value:
            nb += 1

    return nb


def nb_in_out_fixed_vertex(links, vertex_id, nb_vertexes):
    result = []
    t = set()

    for i in links:
        t.add(i.time)

    # computing for each time isn't efficient
    for i in t:
        tmp_links = filter(lambda e: e.time < i, links)
        if len(tmp_links) > 0:
            tmp_res = compute_nb_in_out(tmp_links, nb_vertexes)
            result.append({"time": i, "nb_in": tmp_res[vertex_id].get(vertex_id)[0],
                           "nb_out": tmp_res[vertex_id].get(vertex_id)[1]})

    return result


def nb_in_out_delta_variance(links, nb_vertexes, instant, delta):
    result_plus_delta = []
    result_minus_delta = []
    result_instant = []

    # print str(links[len(links)-1].time) + " " + str(links[0].time)
    if instant - instant < links[len(links)-1].time or delta + instant > links[0].time:
        raise Exception("Make sure delta-instant > 0 and delta+instant < tmax")

    tmp = filter(lambda e: e.time < instant, links)
    tmp_plus = filter(lambda e: instant-delta < e.time <= instant, links)
    tmp_minus = filter(lambda e: instant-delta < e.time <= instant+delta, links)

    tmp_i = compute_nb_in_out(tmp, nb_vertexes)
    tmp_p = compute_nb_in_out(tmp_minus, nb_vertexes)
    tmp_m = compute_nb_in_out(tmp_plus, nb_vertexes)

    for i in range(nb_vertexes):
        result_minus_delta.append({"nb_in": tmp_m[i].get(i)[0], "nb_out": tmp_m[i].get(i)[1]})
        result_plus_delta.append({"nb_in": tmp_p[i].get(i)[0], "nb_out": tmp_p[i].get(i)[1]})
        result_instant.append({"nb_in": tmp_i[i].get(i)[0], "nb_out": tmp_i[i].get(i)[1]})

    return result_minus_delta, result_plus_delta, result_instant

