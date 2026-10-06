"""p13 组合计数：输出 C(n, k) 的精确值（不取模，Python 大整数直接算）。
math.comb 内部就是按最小对称性算的；k 超出 0..n 时按定义是 0。
"""
import sys
from math import comb


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, k = int(data[0]), int(data[1])
    if k < 0 or k > n:
        print(0)
    else:
        print(comb(n, k))


main()
