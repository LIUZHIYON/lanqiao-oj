"""p49 蛇形填数：把 1,2,3,... 沿反对角线（行号 + 列号为定值的一条斜线）依次填进方格，
同一条斜线上从最上面那行开始往下填。给出行列（都从 1 开始），输出那一格的数。
公式：s = row + col，前 s-2 条斜线一共填了 1+2+...+(s-2) = (s-2)(s-1)/2 个数，
      本条斜线上这一格排在第 row 个，所以值 = (s-2)(s-1)//2 + row。
行列不太大时真的模拟填一遍，两种办法必须一致。
"""
import sys


def by_formula(row, col):
    s = row + col
    return (s - 2) * (s - 1) // 2 + row


def by_simulation(row, col):
    """照着规则一格一格填，返回 {(行, 列): 数值} 里目标格的值。"""
    g = {}
    val = 1
    for s in range(2, row + col + 1):
        for i in range(1, s):                 # 行号递增，列 = s - i
            g[(i, s - i)] = val
            val += 1
    return g[(row, col)]


def solve(row, col):
    ans = by_formula(row, col)
    if row + col <= 400:                      # 模拟法代价是 O(s^2)，只在小格子上跑
        assert by_simulation(row, col) == ans, "模拟填数与公式不一致"
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    row, col = int(data[0]), int(data[1])
    print(solve(row, col))


main()
