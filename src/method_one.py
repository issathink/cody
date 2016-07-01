import tool


def compute_nb_in_out(filename, instant):
    result = []
    (links, vertexes) = tool.get_time_links(filename, instant)
    nb_vertexes = len(vertexes)
    res_in = compute_nb_in_out_intermediate(links, nb_vertexes)
    (links, vertexes) = tool.get_time_links(filename, instant, True)
    nb_vertexes = len(vertexes)
    res_out = compute_nb_in_out_intermediate(links, nb_vertexes)

    for i in range(nb_vertexes):
        result.append({i: (res_in[i].get(i)[0], res_out[i].get(i)[1])})

    return result


def compute_nb_in_out_intermediate(links, nb_vertexes):
    if len(links) <= 0:
        raise Exception("Help! links is empty!")

    cur_time = -1
    mat = [[0]*nb_vertexes for _ in range(nb_vertexes)]
    mat_prev = [[0]*nb_vertexes for _ in range(nb_vertexes)]
    result = []

    # why ???
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

        mat[elem.node_a][elem.node_b] = cur_time
        mat[elem.node_b][elem.node_a] = cur_time

        for i in range(nb_vertexes):
            if (i != elem.node_a) and (i != elem.node_b):
                if mat_prev[elem.node_a][i] != -1:
                    if mat_prev[elem.node_b][i] != -1:
                        if mat[elem.node_a][i] > mat_prev[elem.node_b][i]:
                            mat[elem.node_a][i] = mat_prev[elem.node_b][i]
                        elif mat[elem.node_b][i] > mat_prev[elem.node_a][i]:
                            mat[elem.node_b][i] = mat_prev[elem.node_a][i]
                    else:
                        if mat[elem.node_b][i] == -1 or mat[elem.node_b][i] > mat_prev[elem.node_a][i]:
                            mat[elem.node_b][i] = mat_prev[elem.node_a][i]
                else:
                    if mat_prev[elem.node_b][i] != -1:
                        if mat[elem.node_a][i] == -1 or mat[elem.node_a][i] > mat_prev[elem.node_b][i]:
                            mat[elem.node_a][i] = mat_prev[elem.node_b][i]

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

        if elem.node_a == vertex_id:
            cur_time = elem.time
            res[elem.node_b] = cur_time
            i_prev = elem.node_b
        elif elem.node_b == vertex_id:
            cur_time = elem.time
            res[elem.node_a] = cur_time
            i_prev = elem.node_a

        prev_time = cur_time
        cur_time = elem.time

        if prev_time != cur_time:
            if i_prev != -1:
                res_prev[i_prev] = res[i_prev]

        #    for i in range(nb_vertexes):
        #        res_prev[i] = res[i]

        if res_prev[elem.node_a] != -1:
            if res_prev[elem.node_b] != -1:
                if res[elem.node_a] > res[elem.node_b]:
                    res[elem.node_a] = res[elem.node_b]
                    i_prev = elem.node_a
                elif res[elem.node_b] > res[elem.node_a]:
                    res[elem.node_b] = res[elem.node_a]
                    i_prev = elem.node_b
            else:
                if res[elem.node_b] == -1 or res[elem.node_b] > res[elem.node_a]:
                    res[elem.node_b] = res_prev[elem.node_a]
                    i_prev = elem.node_b
        else:
            if res_prev[elem.node_b] != -1:
                if res[elem.node_a] == -1 or res[elem.node_a] > res_prev[elem.node_b]:
                    res[elem.node_a] = res_prev[elem.node_b]
                    i_prev = elem.node_a

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

        if elem.node_a == vertex_id:
            cur_time = elem.time
            res[elem.node_b] = cur_time
        elif elem.node_b == vertex_id:
            cur_time = elem.time
            res[elem.node_a] = cur_time

        prev_time = cur_time
        cur_time = elem.time

        if prev_time != cur_time:
            for i in range(nb_vertexes):
                res_prev[i] = res[i]

        if res_prev[elem.node_a] != -1:
            if res_prev[elem.node_b] != -1:
                if res[elem.node_a] > res[elem.node_b]:
                    res[elem.node_a] = res[elem.node_b]
                elif res[elem.node_b] > res[elem.node_a]:
                    res[elem.node_b] = res[elem.node_a]
            else:
                if res[elem.node_b] == -1 or res[elem.node_b] > res[elem.node_a]:
                    res[elem.node_b] = res_prev[elem.node_a]
        else:
            if res_prev[elem.node_b] != -1:
                if res[elem.node_a] == -1 or res[elem.node_a] > res_prev[elem.node_b]:
                    res[elem.node_a] = res_prev[elem.node_b]

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


def nb_in_out_distribution(result, value, in_out):
    nb = 0

    for i in range(len(result)):
        if in_out is not None and result[i].get(i)[0] == value:
            nb += 1
        elif in_out is None and result[i].get(i)[1] == value:
            nb += 1

    return nb


def nb_in_out_fixed_vertex(filename, vertex_id, each):
    result = []
    t = set()
    (links, vertexes) = tool.get_time_links("./data/" + filename)

    for i in links:
        t.add(i.time)
    t = list(t)

    # computing for each time isn't efficient
    for i in range(t[1], t[-1], each):
        # tmp_res = compute_nb_in_out_array(tmp_links, nb_vertexes)
        tmp_res = compute_nb_in_out("./data/" + filename, i)
        result.append({"time": i, "nb_in": tmp_res[vertex_id].get(vertex_id)[0],
                       "nb_out": tmp_res[vertex_id].get(vertex_id)[1]})
        print "> " + str(i)
    return result


def nb_in_out_delta(filename, instant, delta):
    result = []
    (links, vertexes) = tool.get_time_links(filename)
    nb_vertexes = len(vertexes)

    links_in = filter(lambda e: instant-delta < e.time < instant, links)
    links_out = filter(lambda e: instant < e.time < instant+delta, links)

    res_in = compute_nb_in_out_intermediate(links_in, nb_vertexes)
    res_out = compute_nb_in_out_intermediate(links_out, nb_vertexes)

    for i in range(nb_vertexes):
        result.append({i: (res_in[i].get(i)[0], res_out[i].get(i)[1])})

    return result


def nb_in_out_delta_variance(links, nb_vertexes, instant, delta):
    result_plus_delta = []
    result_minus_delta = []
    result_instant = []

    # print str(links[len(links)-1].time) + " " + str(links[0].time)
    if instant - instant < links[-1].time or delta + instant > links[0].time:
        raise Exception("Make sure delta-instant > 0 and delta+instant < tmax")

    tmp = filter(lambda e: e.time < instant, links)
    tmp_plus = filter(lambda e: instant-delta < e.time <= instant, links)
    tmp_minus = filter(lambda e: instant-delta < e.time <= instant+delta, links)

    # tmp_i = compute_nb_in_out(tmp, nb_vertexes)
    # tmp_p = compute_nb_in_out(tmp_minus, nb_vertexes)
    # tmp_m = compute_nb_in_out(tmp_plus, nb_vertexes)
    tmp_i = compute_nb_in_out_array(tmp, nb_vertexes)
    tmp_p = compute_nb_in_out_array(tmp_minus, nb_vertexes)
    tmp_m = compute_nb_in_out_array(tmp_plus, nb_vertexes)

    for i in range(nb_vertexes):
        result_minus_delta.append({"nb_in": tmp_m[i].get(i)[0], "nb_out": tmp_m[i].get(i)[1]})
        result_plus_delta.append({"nb_in": tmp_p[i].get(i)[0], "nb_out": tmp_p[i].get(i)[1]})
        result_instant.append({"nb_in": tmp_i[i].get(i)[0], "nb_out": tmp_i[i].get(i)[1]})

    return result_minus_delta, result_plus_delta, result_instant

