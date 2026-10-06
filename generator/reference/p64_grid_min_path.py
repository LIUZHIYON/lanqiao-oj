"""p64 方格取数：n 行 m 列的数字表，从左上角走到右下角，只能向右或向下，
把走过的格子里的数都加起来，求最小的总和。
网格 DP：dp[i][j] 只可能从上面或左边过来，取两者较小的再加上本格。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    a = [[int(data[2 + i * m + j]) for j in range(m)] for i in range(n)]
    assert len(data) == 2 + n * m, "格子里的数个数和 n*m 对不上"

    big = 10 ** 15
    dp = [[big] * m for _ in range(n)]
    dp[0][0] = a[0][0]
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                continue
            best = big
            if i > 0 and dp[i - 1][j] < best:
                best = dp[i - 1][j]
            if j > 0 and dp[i][j - 1] < best:
                best = dp[i][j - 1]
            dp[i][j] = best + a[i][j]

    if n <= 8 and m <= 8:         # 小格子直接枚举所有走法核对（只有向右/向下，走法不多）
        brute = []
        for mask in range(1 << (n + m - 2)):
            bits = bin(mask).count("1")
            if bits != n - 1:     # 1 表示向下，必须正好向下 n-1 次
                continue
            seq = [(0, 0)]
            i = j = 0
            ok = True
            for b in range(n + m - 2):
                if mask >> b & 1:
                    i += 1
                else:
                    j += 1
                if i >= n or j >= m:
                    ok = False
                    break
                seq.append((i, j))
            if ok:
                brute.append(sum(a[x][y] for x, y in seq))
        assert dp[n - 1][m - 1] == min(brute), "递推与枚举走法不一致"

    print(dp[n - 1][m - 1])


main()
