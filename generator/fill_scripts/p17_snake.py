"""p17 填空：蛇形填数（沿反对角线、每条斜线从上往下填），第 20 行第 20 列是多少。
真模拟填一遍和套公式，两边必须一致。
"""


def build_grid(max_diag):
    g = {}
    val = 1
    for s in range(2, max_diag + 1):          # s = 行号 + 列号
        for i in range(1, s):
            g[(i, s - i)] = val
            val += 1
    return g


def formula(row, col):
    s = row + col                              # 第 s 条斜线
    return (s - 2) * (s - 1) // 2 + row        # 前 s-2 条斜线共 (s-2)(s-1)/2 个数


g = build_grid(40)
for r in range(1, 21):
    for c in range(1, 21):
        assert g[(r, c)] == formula(r, c), (r, c)
print(formula(20, 20))
