"""p73 连续 k 个数的最大和（滑动窗口入门）：
长度为 n 的数组里，找连续 k 个加起来最大的一段，输出这个和以及它从左数第几个开始（1 起）。
窗口每往右挪一格，就和变成"加上进来的那个、减去掉出去的那个"，不用重算 k 个。
和相同的时候取最靠左的那一段。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    assert len(a) == n, "个数和 n 对不上"
    assert 1 <= k <= n, "k 必须在 1 到 n 之间"

    window = sum(a[:k])
    best = window
    start = 1                         # 记下标时用"第几个"，从 1 数起
    for i in range(k, n):             # 窗口右端挪到第 i 个数（下标从 0 算）
        window += a[i] - a[i - k]
        if window > best:             # 严格大于，保证平局时留最靠左的
            best = window
            start = i - k + 2         # 这一段最左边那个数的下标是 i-k+1，换成"第几个"再加 1

    brute = None                      # 暴力：每个起点都把 k 个加一遍
    for s in range(0, n - k + 1):
        v = sum(a[s:s + k])
        if brute is None or v > brute:
            brute = v
    assert best == brute, "滑动窗口与逐段相加不一致"
    assert start == min(
        s + 1 for s in range(n - k + 1) if sum(a[s:s + k]) == best), "起点不是最靠左的那一段"

    print(best, start)


main()
