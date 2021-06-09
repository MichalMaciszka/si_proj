import random


def pre_clastering(offers, hist, text):
    val = 0.99*hist - 0.04*text
    original = offers.copy()
    result = []
    while len(original) > 0:
        r = random.choice(original)
        original.remove(r)
        tmp = [r]
        for x in original.copy():
            a, b = r.compare_offer(x)
            s = (a*hist + b*text)/(hist + text)
            if s >= val:
                print(s)
                print(r, x)
                tmp.append(x)
                original.remove(x)
        result.append(tmp)
    return result


def construct_array(claster_list, hist, text):
    res = []
    for i in range(len(claster_list)):
        tmp = []
        for j in range(len(claster_list)):
            if i != j:
                tmp.append(claster_list[i].compare(claster_list[j], hist, text))
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


def algorithm(clasters, hist, text, progressBar, num):
    c = clasters.copy()
    l = len(c) / num
    # print("l = ", l)
    result = []
    # while len(c) > num:
    while len(result) < num - 1 and len(c) > 5:
        p = construct_array(c, hist, text)
        x, y = get_max_i_j(p)
        c[x].list.extend(c[y].list.copy())
        print(p[x][y])
        c.pop(y)
        if len(c[x].list) >= l:
            result.append(c[x])
            c.pop(x)
        progressBar.setProperty("value", 40 + (num / len(c) * 50))
    tmp = c[0]
    c.pop(0)
    for e in c:
        tmp.list.extend(e.list)
    result.append(tmp)
    return result
