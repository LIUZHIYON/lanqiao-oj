"""p22 填空：20x20 的方格网，从左上角走到右下角（只能向右或向下），一共多少条路径。
DP 递推一遍，再用组合数 C(40, 20) 算一遍，两边必须一致。
"""
from math import comb

N = M = 20
dp = [[0] * (M + 1) for _ in range(N + 1)]
dp[0][0] = 1
for i in range(N + 1):
    for j in range(M + 1):
        if i == 0 and j == 0:
            continue
        v = 0
        if i > 0:
            v += dp[i - 1][j]
        if j > 0:
            v += dp[i][j - 1]
        dp[i][j] = v
by_dp = dp[N][M]
by_comb = comb(N + M, N)
assert by_dp == by_comb, (by_dp, by_comb)
print(by_dp)
