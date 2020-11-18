from itertools import combinations
import copy


def combination(li, n):
    le = len(li)
    re_li = []
    if le <= n:
        re_li.append(li)
    else:
        t = combinations(li, n)
        for i in t:
            re_it = []
            for j in i:
                re_it.append(j)
            re_li.append(re_it)
    return re_li


def sublist(lia, lib):
    re_li = []
    for it in lia:
        if it not in lib:
            re_li.append(it)
    return re_li


def addlist(lia, lib):
    re_li = lia
    for it in lib:
        if it not in lia:
            re_li.append(it)
    return re_li


def ti(li, di):
    time = 0
    for it in li:
        # time = di[it] if di[it] > time
        if di[it] > time:
            time = di[it]
    return time


def save(li, di):
    with open("01_01.txt", "w") as f:
        for it in li:
            time = ti(it[0], di) + di[it[1]] + ti(it[2], di) + di[it[3]] + ti(it[4], di)
            row = it[0][0]+it[0][1]+","+it[1]+","+it[2][0]+it[2][1]+","+it[3]+","+it[4][0]+it[4][1]+","+str(time)+",\n"
            f.write(row)


def main():
    per = ['A', 'B', 'C', 'D']
    di = {
        'A': 1, 'B': 2, 'C': 5, 'D': 10
    }
    t1 = combination(per, 2)
    li_node = []
    for ia in t1:
        for ib in ia:
            left = []
            right = []
            left = addlist(left, sublist(per, ia))
            right = addlist(right, ia)
            left = addlist(left, ib)
            right.remove(ib)
            t2 = combination(left, 2)
            for ic in t2:
                right = []
                right = addlist(right, ia)
                right.remove(ib)
                right = addlist(right, ic)
                for id in right:
                    left = []
                    right = []
                    left = addlist(left, sublist(per, ia))
                    right = addlist(right, ia)
                    left = addlist(left, ib)
                    right.remove(ib)
                    left = sublist(left, ic)
                    right = addlist(right, ic)
                    left.append(id)
                    right.remove(id)
                    ie = left
                    tree = [ia, ib, ic, id, ie]
                    li_node.append(tree)
    for it in li_node:
        print(it)
    print(len(li_node))
    save(li_node, di)


if __name__ == "__main__":
    main()

"""
    for ia in t1:
        for ib in ia:
            left = []
            right = []
            left = addlist(left, sublist(per, ia))
            right = addlist(right, ia)
            left = addlist(left, ib)
            right.remove(ib)
            t2 = combination(left, 2)
            for ic in t2:
                right = []
                right = addlist(right, ia)
                right.remove(ib)
                right = addlist(right, ic)
                for id in right:
                    left = []
                    right = []
                    left = addlist(left, sublist(per, ia))
                    right = addlist(right, ia)
                    left = addlist(left, ib)
                    right.remove(ib)
                    left = sublist(left, ic)
                    right = addlist(right, ic)
                    left.append(id)
                    right.remove(id)
                    ie = left
                    tree = [ia, ib, ic, id, ie]
                    li_node.append(tree)

"""
"""
    for ia in t1:
        left = []
        right = []
        left = addlist(left, sublist(per, ia))
        right = addlist(right, ia)
        temp_left = left.copy()
        temp_right = right.copy()
        for ib in ia:
            left = temp_left
            right = temp_right
            left = addlist(left, ib)
            right.remove(ib)
            temp_left_2 = left.copy()
            temp_right_2 = right.copy()
            t2 = combination(left, 2)
            for ic in t2:
                left = temp_left_2
                right = temp_right_2
                left = sublist(left, ic)
                right = addlist(right, ic)
                temp_left_3 = left.copy()
                temp_right_3 = right.copy()
                for id in right:
                    left = temp_left_3
                    right = temp_right_3
                    left.append(id)
                    right.remove(id)
                    ie = left
                    tree = [ia, ib, ic, id, ie]
                    li_node.append(tree)

"""
"""
    for ia in t1:
        left = []
        right = []
        left = addlist(left, sublist(per, ia))
        right = addlist(right, ia)
        temp_left = left.copy()
        temp_right = right.copy()
        for ib in ia:
            temp_left = addlist(temp_left, ib)
            temp_right.remove(ib)
            temp_left_2 = temp_left.copy()
            temp_right_2 = temp_right.copy()
            t2 = combination(left, 2)
            for ic in t2:
                temp_left_2 = sublist(temp_left_2, ic)
                temp_right_2 = addlist(temp_right_2, ic)
                temp_left_3 = temp_left_2.copy()
                temp_right_3 = temp_right_2.copy()
                for id in right:
                    temp_left_3.append(id)
                    temp_right_3.remove(id)
                    ie = temp_left_3
                    tree = [ia, ib, ic, id, ie]
                    li_node.append(tree)

"""
"""
    for ia in t1:
        left = []
        right = []
        left = addlist(left, sublist(per, ia))
        right = addlist(right, ia)
        temp_left = copy.copy(left)
        temp_right = copy.copy(right)
        for ib in ia:
            left = temp_left
            right = temp_right
            left = addlist(left, ib)
            right.remove(ib)
            temp_left_2 = copy.copy(left)
            temp_right_2 = copy.copy(right)
            t2 = combination(left, 2)
            for ic in t2:
                left = temp_left_2
                right = temp_right_2
                left = sublist(left, ic)
                right = addlist(right, ic)
                temp_left_3 = copy.copy(left)
                temp_right_3 = copy.copy(right)
                for id in right:
                    left = temp_left_3
                    right = temp_right_3
                    left.append(id)
                    right.remove(id)
                    ie = left
                    tree = [ia, ib, ic, id, ie]
                    li_node.append(tree)

"""