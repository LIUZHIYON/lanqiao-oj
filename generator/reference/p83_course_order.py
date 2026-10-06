"""p83 选课顺序（拓扑排序提高）：
n 门课，m 条例子"先学 a 才能学 b"，要给出一个能上完所有课的顺序，
同样能上完的时候挑字典序最小的那个（也就是每一步都挑当下编号最小的可选课）；
有环、根本排不出来时输出 -1。
入度表 + Kahn：入度为 0 的课随时能上，上一门就把它的后继入度减 1，
减到 0 又变成可选。最后排出来的门数不到 n，就说明课里绕成了环。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    pos = 2
    for _ in range(m):
        a, b = int(data[pos]), int(data[pos + 1])
        pos += 2
        adj[a].append(b)              # a 是 b 的先修课
        indeg[b] += 1

    order = []
    taken = [False] * (n + 1)
    for _ in range(n):                # 每轮线性扫一遍，挑编号最小的入度 0 课程
        pick = 0
        for i in range(1, n + 1):
            if indeg[i] == 0 and not taken[i]:
                pick = i
                break                 # 从 1 开始扫，第一个能选的就是编号最小的
        if pick == 0:
            print(-1)                 # 一门都选不出来，剩下的全卡在环里
            return
        taken[pick] = True
        order.append(pick)
        for v in adj[pick]:
            indeg[v] -= 1

    assert len(order) == n, "排出来的门数不对"
    if n <= 60:                       # 小图再检查每条先修关系有没有被排在前面
        place = {c: i for i, c in enumerate(order)}
        for i in range(1, n + 1):
            for v in adj[i]:
                assert place[i] < place[v], "先修课排到了后面"
    sys.stdout.write(" ".join(map(str, order)) + "\n")


main()
