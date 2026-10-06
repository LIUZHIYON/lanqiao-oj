"""p05 迷宫最短路：0 是路 1 是墙，从左上角走到右下角，每步走相邻一格。
BFS 一层一层往外扩，第一次到达终点的那一层就是最少步数。
"""
import sys
from collections import deque

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # 上 下 左 右


def bfs_steps(grid, n, m):
    if grid[0][0] == '1' or grid[n - 1][m - 1] == '1':
        return -1
    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 0
    if n == 1 and m == 1:
        return 0                # 起点就是终点，走了 0 步
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()          # 必须 popleft，用 pop 就变成深度优先了
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == '0' \
                    and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                if nx == n - 1 and ny == m - 1:
                    return dist[nx][ny]
                q.append((nx, ny))
    return -1


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]
    print(bfs_steps(grid, n, m))


main()
