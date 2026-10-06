"""p60 零钱兑换：给 k 种面额（每种想用多少次都行），凑出金额 s 最少要几枚硬币，
凑不出来输出 -1。
完全背包：dp[j] = 凑出 j 的最少枚数，dp[0] = 0，其余先记成"不可能"。
外层枚举面额、内层金额从小到大走，这样同一种面额可以重复取。
金额小的时候用广度优先（每次往外加一枚硬币）核对，两条路都得给同一个答案。
"""
import sys
from collections import deque


def min_coins(coins, s):
    inf = s + 1                               # 最多也就是 s 枚 1 元，比 s 大就代表不可能
    dp = [inf] * (s + 1)
    dp[0] = 0
    for c in coins:
        if c > s:
            continue
        for j in range(c, s + 1):             # 正序 = 同一种面额可以多次用
            v = dp[j - c] + 1
            if v < dp[j]:
                dp[j] = v
    return -1 if dp[s] > s else dp[s]


def by_bfs(coins, s):
    if s == 0:
        return 0
    step = [-1] * (s + 1)
    step[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        for c in coins:
            v = u + c
            if v <= s and step[v] < 0:
                step[v] = step[u] + 1
                if v == s:
                    return step[v]
                q.append(v)
    return -1


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    k, s = int(data[0]), int(data[1])
    coins = [int(x) for x in data[2:2 + k]]
    assert len(coins) == k, "面额个数和 k 对不上"
    coins = sorted(set(c for c in coins if c > 0))
    ans = min_coins(coins, s)
    if s <= 2000:                             # BFS 是 O(s*k)，小规模核对用
        assert ans == by_bfs(coins, s), "背包与 BFS 不一致"
    print(ans)


main()
