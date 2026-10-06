"""p70 排队改数（差分入门）：q 次操作，每次把第 l 到第 r 个格子都加 v，
全部做完后输出整个数组。
差分做法：d[l] += v、d[r+1] -= v，两次单点改动顶掉一段；
最后从左边一路累加 d，走到第 i 个位置累计到的就是它的总增量。
这题数据小，所以顺手用"老老实实一格一格改"的朴素写法核对一遍。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, q = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    assert len(a) == n, "数组长度和 n 对不上"

    d = [0] * (n + 2)                 # 多开一格放 r+1 的减记，越界判断就省了
    ops = []
    pos = 2 + n
    for _ in range(q):
        l, r, v = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        assert 1 <= l <= r <= n, "区间下标不合法"
        d[l] += v
        d[r + 1] -= v
        ops.append((l, r, v))

    slow = list(a)                    # 朴素：一次操作改一段
    for l, r, v in ops:
        for i in range(l - 1, r):
            slow[i] += v

    out = []
    add = 0
    for i in range(1, n + 1):
        add += d[i]
        out.append(str(a[i - 1] + add))
    assert out == [str(x) for x in slow], "差分与逐格修改不一致"
    sys.stdout.write(" ".join(out) + "\n")


main()
