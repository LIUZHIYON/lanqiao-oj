"""p76 分跳绳（二分答案入门）：
n 根绳子，要剪出 k 段一样长的整数长度绳子，不许拼接、不许浪费以外的要求，
问每段最长能是多少；连长度 1 都凑不够 k 段时输出 0。
"长度越长，能剪出的段数越少"，可行性随长度单调，所以可以对答案二分。
这里长度上限只有一千，直接一个一个试也能试出来，两种写法都跑一遍核对。
"""
import sys


def pieces(a, x):
    return sum(v // x for v in a)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    assert len(a) == n, "绳子根数和 n 对不上"
    assert k >= 1, "k 至少是 1"

    if pieces(a, 1) < k:              # 剪成 1 长都凑不够，怎么剪都不行
        print(0)
        return

    lo, hi = 1, max(a)
    while lo < hi:                    # mid = (lo + hi + 1) // 2 配 lo = mid，
        mid = (lo + hi + 1) // 2      # 少写那个 +1 就会原地打转
        if pieces(a, mid) >= k:
            lo = mid
        else:
            hi = mid - 1

    brute = 0                         # 一个一个长度试过去，小规模完全够
    for x in range(1, max(a) + 1):
        if pieces(a, x) >= k:
            brute = x
    assert lo == brute, "二分答案与逐一试不一致"

    print(lo)


main()
