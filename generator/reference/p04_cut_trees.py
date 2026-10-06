"""p04 砍树：求最高的锯木高度 H，使切下的木材总量不少于 M。
H 越高得到的木材越少，有单调性 -> 二分答案。check(H) 用 O(n) 累加。
"""
import sys


def wood_at(heights, h):
    return sum(x - h for x in heights if x > h)


def max_height(heights, m):
    if wood_at(heights, 0) < m:     # 连地面都锯不够 M，无解（按 0 输出）
        return 0
    lo, hi = 0, max(heights)
    while lo < hi:
        mid = (lo + hi + 1) // 2    # +1 配合 lo = mid，否则会死循环
        if wood_at(heights, mid) >= m:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    heights = [int(x) for x in data[2:2 + n]]
    print(max_height(heights, m))


main()
