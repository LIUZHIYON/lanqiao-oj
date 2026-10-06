"""p67 水田块数（DFS 网格 / flood fill 入门）：
1 是水田，0 是旱地，上下左右挨着的水田算同一块。输出块数和最大一块的格数。
从一个没看过的格子出发，用栈把所有能走到的 1 都标记掉，这就是一次深度优先搜索；
一共启动几次，就有几块田。写成递归在 30x30 上也行，但换成显式栈更保险。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]
    assert len(grid) == n and all(len(row) == m for row in grid), "网格行列数对不上"

    seen = [[False] * m for _ in range(n)]
    blocks = 0
    biggest = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] != "1" or seen[i][j]:
                continue
            blocks += 1                       # 又发现一块没见过的田
            cnt = 0
            stack = [(i, j)]
            seen[i][j] = True                 # 进栈就标记，否则同一格会被反复塞进栈
            while stack:
                x, y = stack.pop()
                cnt += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m:
                        if grid[nx][ny] == "1" and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
            if cnt > biggest:
                biggest = cnt

    assert sum(row.count("1") for row in grid) == sum(
        1 for i in range(n) for j in range(m) if seen[i][j]), "有格子没被走到"
    print(blocks, biggest)


main()
