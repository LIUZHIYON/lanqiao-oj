"""p55 二维前缀和：给 n 行 m 列的矩阵和 q 个子矩阵询问，输出每个子矩阵的元素和。
ps[i][j] = 左上角到 (i, j) 这个矩形的和，递推
    ps[i][j] = ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1] + a[i][j]
询问 [r1,c1]-[r2,c2] 用容斥：大矩形减上块减左块加回左上块。
行列都从 1 开始编号，第 0 行第 0 列留 0，就不用特判边界。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = [int(x) for x in data]
    n, m = it[0], it[1]
    a = []
    pos = 2
    for _ in range(n):
        a.append(it[pos:pos + m])
        pos += m

    ps = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        row = a[i - 1]
        cur = ps[i]
        prev = ps[i - 1]
        run = 0
        for j in range(1, m + 1):
            run += row[j - 1]                 # 本行前 j 个之和
            cur[j] = prev[j] + run            # 上面那块 + 这一行新增的一条
    assert ps[n][m] == sum(sum(r) for r in a), "整块和对不上"

    q = it[pos]
    pos += 1
    small = q <= 30 and n * m <= 10000        # 小数据直接一层层加，核对用
    out = []
    for _ in range(q):
        r1, c1, r2, c2 = it[pos], it[pos + 1], it[pos + 2], it[pos + 3]
        pos += 4
        v = ps[r2][c2] - ps[r1 - 1][c2] - ps[r2][c1 - 1] + ps[r1 - 1][c1 - 1]
        if small:
            direct = 0
            for i in range(r1 - 1, r2):
                direct += sum(a[i][c1 - 1:c2])
            assert v == direct, "前缀和与直接相加不一致"
        out.append(str(v))
    sys.stdout.write("\n".join(out) + "\n")


main()
