"""p57 单源最短路：带权有向图（边权非负），给起点 s，按编号 1..n 输出到每个点的最短距离，
走不到输出 -1。
堆优化 Dijkstra：小根堆里放 (当前距离, 点)，每次取出还没定下来的最近点。
同一个点会被塞进堆好几次，出队时用 if d > dist[u]: continue 把旧记录丢掉。
点少的时候用 O(n^2) 每轮扫一遍最小值的朴素做法核对。
"""
import sys
import heapq

INF = 10 ** 30


def dijkstra(n, adj, s):
    dist = [INF] * (n + 1)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                       # 过期记录，跳过
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def dijkstra_naive(n, adj, s):
    """不用堆，每轮线性找未确定点里距离最小的那个。"""
    dist = [INF] * (n + 1)
    dist[s] = 0
    done = [False] * (n + 1)
    for _ in range(n):
        u = 0
        best = INF
        for i in range(1, n + 1):
            if not done[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == 0:
            break
        done[u] = True
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


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
        adj[u].append((v, w))                 # 有向边；重边留着不影响正确性
    dist = dijkstra(n, adj, s)
    if n <= 300:                              # 小图拿朴素 Dijkstra 核对
        assert dist == dijkstra_naive(n, adj, s), "堆优化与朴素 Dijkstra 不一致"
    out = [str(dist[i] if dist[i] < INF else -1) for i in range(1, n + 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
