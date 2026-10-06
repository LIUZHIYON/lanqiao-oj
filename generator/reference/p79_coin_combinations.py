"""p79 凑零钱的方案数（完全背包计数提高）：
k 种面额互不相同的硬币，每种想用几枚都行，问凑出金额 s 一共有多少种凑法。
只看每种面额用了几枚，不看拿的先后，所以"1 枚 2 角 + 2 枚 1 角"和
"2 枚 1 角 + 1 枚 2 角"只算同一种。
外层循环必须枚举面额、内层枚举金额，这样数出来的才是凑法而不是顺序
（外层换成金额就变成数顺序了，是这类题最容易踩的坑）。
dp[j] = 凑出金额 j 的凑法数，dp[0] = 1（一枚都不拿也算一种）。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    k, s = int(data[0]), int(data[1])
    coins = [int(x) for x in data[2:2 + k]]
    assert len(coins) == k, "面额个数和 k 对不上"
    assert len(set(coins)) == k, "面额互不相同"
    coins.sort()

    dp = [0] * (s + 1)
    dp[0] = 1
    for c in coins:                   # 外层是面额：一次只考虑一种
        for j in range(c, s + 1):     # 金额从小到大：同一面额才能反复用
            dp[j] += dp[j - c]

    if s <= 30 and k <= 6:            # 小规模再按"每种用几枚"递归硬数一遍核对
        cnt = 0

        def dfs(idx, left):
            nonlocal cnt
            if idx == k:
                if left == 0:
                    cnt += 1
                return
            use = 0
            while use * coins[idx] <= left:
                dfs(idx + 1, left - use * coins[idx])
                use += 1

        dfs(0, s)
        assert cnt == dp[s], "背包计数与递归硬数不一致"

    print(dp[s])


main()
