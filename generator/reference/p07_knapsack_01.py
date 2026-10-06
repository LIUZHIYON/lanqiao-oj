"""p07 0-1 背包：容量 W，每件物品最多选一次，求能装下的最大价值。
一维滚动数组 dp[c] = 容量 c 时的最大价值；内层必须从大到小遍历，
这样每个物品只会被用一次（从小到大就会重复取同一件）。
"""
import sys


def knapsack(items, w_cap):
    dp = [0] * (w_cap + 1)
    for weight, value in items:
        if weight > w_cap:
            continue
        for c in range(w_cap, weight - 1, -1):     # 逆序！
            nv = dp[c - weight] + value
            if nv > dp[c]:
                dp[c] = nv
    return dp[w_cap]


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, w_cap = int(data[0]), int(data[1])
    items = []
    pos = 2
    for _ in range(n):
        items.append((int(data[pos]), int(data[pos + 1])))
        pos += 2
    print(knapsack(items, w_cap))


main()
