"""p75 小镇观光（Dijkstra 入门）：n 个点、m 条双向道路，长度都非负，
从 s 出发，按编号 1 到 n 输出到每个点的最短距离，到不了输出 -1。
这里用每轮线性扫一遍找最小距离的朴素写法，复杂度 O(n^2)，点少的时候完全够用。
再用小根堆优化的写法算一遍，两边必须一致。
"""
import heapq
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m, s = int(data[0]), int(data[1]), int(data[2])
    adj = [[] for _ in range(n + 1)]
    pos = 3
    for _ in range(m):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))         # 双向道路
        adj[v].append((u, w))
    assert pos == len(data), "边数对不上"

    big = 10 ** 18
    INF = big
    dist = [INF] * (n + 1)
    used = [False] * (n + 1)
    dist[s] = 0
    for _ in range(n):                # 每轮定下一个最远的点
        u = 0
        best = INF
        for i in range(1, n + 1):     # 线性扫最小值，朴素版就是这么慢
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == 0:
            break                     # 剩下的点都到不了
        used[u] = True
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    heap_dist = [INF] * (n + 1)       # 堆优化版，拿来核对
    heap_dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > heap_dist[u]:
            continue                  # 堆里留下的旧记录，跳过
        for v, w in adj[u]:
            if d + w < heap_dist[v]:
                heap_dist[v] = d + w
                heapq.heappush(heap, (heap_dist[v], v))

    assert dist == heap_dist, "朴素 Dijkstra 与堆优化不一致"
    out = []
    for i in range(1, n + 1):
        out.append(str(dist[i] if dist[i] < big else -1))
    sys.stdout.write("\n".join(out) + "\n")


main()
