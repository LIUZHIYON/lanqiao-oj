"""p74 合并与查询（并查集入门）：
操作 1 a b 把 a、b 合并到同一组；操作 2 a b 问 a、b 是否同组，输出 yes 或 no；
全部操作做完，最后一行输出还剩多少个组。
find 找根：一路 parent[x] = x 往上走到根。这里用循环加路径减半，别写成深层递归。
组数一开始是 n，每次真的把两个不同的根合起来才减 1。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, q = int(data[0]), int(data[1])
    parent = list(range(n))
    size = [1] * n                    # size 只有根上才是这一组的真实人数

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]     # 路径减半：往上跳一格
            x = parent[x]
        return x

    groups = n
    out = []
    pos = 2
    for _ in range(q):
        op = int(data[pos])
        a = int(data[pos + 1]) - 1
        b = int(data[pos + 2]) - 1
        pos += 3
        assert pos <= len(data), "操作行数不够"
        ra, rb = find(a), find(b)
        if op == 1:
            if ra != rb:              # 已经同组就什么都不用做
                if size[ra] < size[rb]:
                    ra, rb = rb, ra   # 小挂到大下面，树才不会退化成一条链
                parent[rb] = ra
                size[ra] += size[rb]
                groups -= 1
        else:
            out.append("yes" if ra == rb else "no")

    # 数根的时候要把每个点都 find 到底，路径压缩过之后父节点不一定是根
    roots = len(set(find(i) for i in range(n)))
    assert roots == groups, "维护的组数与实际根数不一致"
    out.append(str(groups))
    sys.stdout.write("\n".join(out) + "\n")


main()
