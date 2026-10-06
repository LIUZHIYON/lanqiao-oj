"""p23 填空：七段数码管（a~g 七个段），点亮若干个段组成一个"字符"。
要求亮着的段必须首尾相连（有公共端点就算相连）。问一共能点亮多少种连通的字符。
枚举 127 个非空子集，每个子集只在"两端都亮着"的边上做连通检查：
做法 A 并查集，做法 B 从任一段出发做广度优先搜索，两边必须一致。
"""
from collections import deque
from itertools import combinations

ADJ = {
    'a': ['b', 'f'],
    'b': ['a', 'g', 'c'],
    'c': ['b', 'g', 'd'],
    'd': ['c', 'e'],
    'e': ['d', 'f', 'g'],
    'f': ['a', 'e', 'g'],
    'g': ['b', 'c', 'e', 'f'],
}
SEGS = ['a', 'b', 'c', 'd', 'e', 'f', 'g']


def connected_dsu(subset):
    if len(subset) <= 1:
        return True
    fa = {x: x for x in subset}

    def find(x):
        while fa[x] != x:
            fa[x] = fa[fa[x]]
            x = fa[x]
        return x

    for u in subset:
        for v in ADJ[u]:
            if v in fa:
                ru, rv = find(u), find(v)
                if ru != rv:
                    fa[rv] = ru
    return len({find(x) for x in subset}) == 1


def connected_bfs(subset):
    if len(subset) <= 1:
        return True
    seen = {subset[0]}
    q = deque([subset[0]])
    while q:
        u = q.popleft()
        for v in ADJ[u]:
            if v in subset and v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == len(subset)


total = 0
for k in range(1, 8):
    for sub in combinations(SEGS, k):
        a, b = connected_dsu(list(sub)), connected_bfs(list(sub))
        assert a == b, sub
        if a:
            total += 1
print(total)
