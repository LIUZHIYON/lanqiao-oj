"""p56 朋友圈：n 个人、m 条认识关系（无向），输出连通块个数和最大块的人数。
并查集：parent 记录每个集合的根，size 只在根上有意义。
find 用循环 + 路径减半（写成递归在几十万人的链上会爆栈），合并时把小的挂到大的下面。
规模小的时候再用邻接表广度优先数一遍核对。
"""
import sys
from collections import deque


def solve(n, pairs):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]     # 路径减半，树越来越扁
            x = parent[x]
        return x

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue                          # 已经在同一个圈里（重边）
        if size[ra] < size[rb]:
            ra, rb = rb, ra                   # 小的挂到大的下面
        parent[rb] = ra
        size[ra] += size[rb]

    comps = 0
    biggest = 0
    for i in range(n):
        if find(i) == i:                      # 只有根代表一个连通块
            comps += 1
            if size[i] > biggest:
                biggest = size[i]
    return comps, biggest


def by_bfs(n, pairs):
    adj = [[] for _ in range(n)]
    for a, b in pairs:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * n
    comps = biggest = 0
    for s in range(n):
        if seen[s]:
            continue
        comps += 1
        cnt = 0
        seen[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            cnt += 1
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        if cnt > biggest:
            biggest = cnt
    return comps, biggest


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    pairs = []
    pos = 2
    for _ in range(m):
        a = int(data[pos]) - 1
        b = int(data[pos + 1]) - 1
        pos += 2
        pairs.append((a, b))
    ans = solve(n, pairs)
    if n <= 2000 and m <= 4000:               # 小数据用广度优先核一遍
        assert ans == by_bfs(n, pairs), "并查集与 BFS 数块不一致"
    print(ans[0], ans[1])


main()
