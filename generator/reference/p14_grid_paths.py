"""p14 网格路径数：0 是空格 1 是墙，从左上角到右下角只能向右或向下，数一数几条路。
dp[i][j] = 到达 (i,j) 的路径数 = 上面来的 + 左边来的；墙的位置直接留 0。
Python 大整数不会溢出，所以路径数可以完整打印出来。
"""
import sys


def count_paths(grid, n, m):
    if grid[0][0] == '1' or grid[n - 1][m - 1] == '1':
        return 0
    dp = [[0] * m for _ in range(n)]
    dp[0][0] = 1
    for i in range(n):
        for j in range(m):
            if (i == 0 and j == 0) or grid[i][j] == '1':
                continue
            v = 0
            if i > 0:
                v += dp[i - 1][j]
            if j > 0:
                v += dp[i][j - 1]
            dp[i][j] = v
    return dp[n - 1][m - 1]


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]
    print(count_paths(grid, n, m))


main()
