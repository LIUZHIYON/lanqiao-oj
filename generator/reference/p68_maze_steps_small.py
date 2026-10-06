"""p68 迷宫最少步（BFS 入门）：从左上角走到右下角，每步只能上下左右挪一格，
墙（1）不能进，走不到输出 -1。
BFS 一层一层往外扩，第一次踩到终点时的层数就是最短步数。
两个要点：用 deque 的 popleft（用 pop 就退化成深度优先，得到的不是最短）；
入队的时候就把距离写上（等出队才标记会让同一格排队好几次）。
"""
import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]
    assert len(grid) == n and all(len(row) == m for row in grid), "网格行列数对不上"

    if grid[0][0] == "1" or grid[n - 1][m - 1] == "1":
        print(-1)                             # 起点或终点本身就是墙，一步也动不了
        return

    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] == "0" and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

    ans = dist[n - 1][m - 1]
    if n <= 10 and m <= 10 and ans >= 0:      # 小图再用每轮扩一层的写法核一遍
        step = 0
        frontier = [(0, 0)]
        visited = {(0, 0)}
        found = -1
        while frontier:
            nxt = []
            for x, y in frontier:
                if (x, y) == (n - 1, m - 1):
                    found = step
                    break
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == "0" \
                            and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        nxt.append((nx, ny))
            if found >= 0:
                break
            step += 1
            frontier = nxt
        assert found == ans, "队列版与按层扩版的步数不一致"
    print(ans)


main()
