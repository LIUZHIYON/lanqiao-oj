"""p65 小背包：容量 W，n 件物品各有重量和价值，每件要么整件拿走要么不要，
求总重量不超过 W 时能装下的最大价值。
物品只有十几件，所以两种写法都跑一遍互相核对：
  · 暴力 dfs：对每件物品问一次"拿还是不拿"，两条分支往下走
  · 一维滚动数组的 0-1 背包：内层容量必须从大到小，否则同一件会被用两次
"""
import sys


def by_dfs(items, W):
    """枚举每件拿不拿，最多 2^n 个叶子。"""
    best = 0

    def dfs(idx, weight, value):
        nonlocal best
        if weight > W:                # 超重了，这一支不用再往下走
            return
        if value > best:
            best = value
        if idx == len(items):
            return
        dfs(idx + 1, weight, value)           # 不要这件
        w, v = items[idx]
        dfs(idx + 1, weight + w, value + v)   # 要这件

    dfs(0, 0, 0)
    return best


def by_dp(items, W):
    dp = [0] * (W + 1)                # dp[c] = 容量为 c 时能装下的最大价值
    for w, v in items:
        for c in range(W, w - 1, -1):  # 从大到小，保证每件最多用一次
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[W]


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, W = int(data[0]), int(data[1])
    items = []
    pos = 2
    for _ in range(n):
        items.append((int(data[pos]), int(data[pos + 1])))
        pos += 2
    assert pos == len(data), "物品行数对不上"

    ans = by_dp(items, W)
    assert ans == by_dfs(items, W), "背包递推与枚举子集不一致"
    print(ans)


main()
