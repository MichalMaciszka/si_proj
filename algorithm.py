def construct_array(claster_list):
    res = []
    for i in range(len(claster_list)):
        tmp = []
        for j in range(len(claster_list)):
            if i != j:
                tmp.append(claster_list[i].compare(claster_list[j]))
            else:
                tmp.append(-1)
        res.append(tmp)
    return res

def get_max_i_j(array):
    val = 0
    max_i = -1
    max_j = -1
    for i in range(len(array)):
        for j in range(len(array)):
            if array[i][j] > val:
                val = array[i][j]
                max_i = i
                max_j = j
    return max_i, max_j

def algorithm(clasters):
    c = clasters.copy()
    while len(c) > 5:
        p = construct_array(c)
        x, y = get_max_i_j(p)
        c[x].list.extend(c[y].list)
        c.pop(y)
    return c