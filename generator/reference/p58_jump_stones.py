"""p58 跳石头：起点 0、终点 L，中间 n 块岩石，最多搬走 m 块，
让"相邻两次落脚的最小间距"尽量大，输出这个最大值。
最大值最小化 -> 二分答案。check(x)：能不能让每一跳都不小于 x？
贪心扫一遍，间距不够就把当前这块搬掉（搬掉的计数超 m 就失败），够了就把落脚点点在这块上。
岩石少时用枚举搬法的方式暴力算一遍核对。
"""
import sys


def feasible(x, points, budget):
    used = 0
    last = points[0]                          # points 里已经含起点 0 和终点 L
    for i in range(1, len(points)):
        if points[i] - last < x:
            used += 1                         # 这块留不住，搬掉
            if used > budget:
                return False
        else:
            last = points[i]                  # 落脚在这块
    return True


def by_binary(n, m, rocks, L):
    points = [0] + rocks + [L]
    lo, hi = 1, L
    while lo < hi:
        mid = (lo + hi + 1) // 2              # +1 配 lo = mid，否则会原地打转
        if feasible(mid, points, m):
            lo = mid
        else:
            hi = mid - 1
    return lo


def by_brute(n, m, rocks, L):
    best = 0
    for mask in range(1 << n):                # 枚举哪些岩石被搬走
        removed = bin(mask).count("1")
        if removed > m:
            continue
        seq = [0]
        for i in range(n):
            if not (mask >> i) & 1:
                seq.append(rocks[i])
        seq.append(L)
        gap = min(seq[i + 1] - seq[i] for i in range(len(seq) - 1))
        if gap > best:
            best = gap
    return best


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    L, n, m = int(data[0]), int(data[1]), int(data[2])
    rocks = sorted(int(x) for x in data[3:3 + n])
    assert len(rocks) == n, "岩石数对不上"
    assert all(0 < rocks[i] < L for i in range(n)) and \
        len(set(rocks)) == n, "岩石必须落在 (0, L) 内且不重叠"
    ans = by_binary(n, m, rocks, L)
    if n <= 12:                               # 暴力枚举搬法是 2^n，只能小规模核
        assert ans == by_brute(n, m, rocks, L), "二分答案与暴力不一致"
    print(ans)


main()
