"""p84 石子合并（区间 DP 较难）：
一排 n 堆石子，每次只能把相邻的两堆合成一堆，这一趟的费用是这两堆的数量之和，
全部合成一堆为止，问总费用最小是多少。
区间 DP：f[i][j] = 把第 i 到第 j 堆合成一堆的最小费用。
最后一步一定是把 [i, k] 和 [k+1, j] 两块并起来，加上这一趟的费用（区间石子总数），
所以 f[i][j] = min over k of f[i][k] + f[k+1][j] + sum(i..j)。
按区间长度从小到大填表，短区间一定先算好。区间和用前缀和 O(1) 拿。
"""
import sys
from functools import lru_cache


def by_brute(piles):
    """独立核对：状态就是当前还剩的这几堆，枚举先合并哪一对相邻的。"""

    @lru_cache(maxsize=None)
    def solve(state):
        if len(state) == 1:
            return 0
        best = None
        for i in range(len(state) - 1):
            merged = state[:i] + (state[i] + state[i + 1],) + state[i + 2:]
            cost = state[i] + state[i + 1] + solve(merged)
            if best is None or cost < best:
                best = cost
        return best

    return solve(tuple(piles))


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    piles = [int(x) for x in data[1:1 + n]]
    assert len(piles) == n, "堆数和 n 对不上"

    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + piles[i]

    def total(i, j):                  # 第 i 到第 j 堆（下标从 0）的总数
        return pre[j + 1] - pre[i]

    f = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):    # 枚举区间长度，短的先算完
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = None
            for k in range(i, j):     # 最后一步在哪条缝上合并
                cost = f[i][k] + f[k + 1][j] + total(i, j)
                if best is None or cost < best:
                    best = cost
            f[i][j] = best

    ans = f[0][n - 1]
    if n <= 9:                        # 只有 9 堆以内才敢用枚举合并顺序硬算
        assert ans == by_brute(tuple(piles)), "区间 DP 与枚举合并顺序不一致"
    print(ans)


main()
