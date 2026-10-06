"""p54 差分区间加：初始数组给定，做 q 次"把第 l 到第 r 个都加 v"，最后输出整个数组。
一段一段改数组是 O(n*q)，太慢。差分把区间加变成两次单点改：
d[l] += v, d[r+1] -= v，最后对 d 求一次前缀和就是每个位置的总增量。
数组小的时候用直接改原数组的办法核对一遍。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, q = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    assert len(a) == n, "数组长度和 n 对不上"

    d = [0] * (n + 1)                         # 多留一格放 r+1 的 -v，省掉越界判断
    ops = []
    pos = 2 + n
    for _ in range(q):
        l, r, v = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        ops.append((l, r, v))
        d[l - 1] += v                         # 下标从 0 数：第 l 个是 l-1
        if r < n:
            d[r] -= v

    res = []
    cur = 0
    for i in range(n):
        cur += d[i]
        res.append(a[i] + cur)

    if n * q <= 100000:                       # 小数据用朴素逐个加核对
        naive = list(a)
        for l, r, v in ops:
            for i in range(l - 1, r):
                naive[i] += v
        assert naive == res, "差分与朴素做法不一致"

    sys.stdout.write(" ".join(map(str, res)) + "\n")


main()
