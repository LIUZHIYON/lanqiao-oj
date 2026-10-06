"""p80 合法括号串计数（卡特兰数提高）：
恰好 n 对括号能拼成多少个合法括号串，输出精确值。
枚举最外面那对括号"里面包了多长"：设 g[i] 是长度 i 的合法串个数（i 只取偶数），
g[0] = 1，第一对括号里有 j 对、后面跟着 i-1-j 对，
所以 g[2i] = Σ g[2j] * g[2(i-1-j)]。
这就是卡特兰数，闭式是 C(2n, n) / (n + 1)，两条路必须给同一个数。
"""
import math
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    assert 1 <= n <= 30, "n 的范围不对"

    g = [0] * (2 * n + 1)
    g[0] = 1
    for pairs in range(1, n + 1):     # pairs 对括号
        total = 0
        for inner in range(pairs):    # 最外那对里面装 inner 对，剩下 pairs-1-inner 对排在后面
            total += g[2 * inner] * g[2 * (pairs - 1 - inner)]
        g[2 * pairs] = total

    formula = math.comb(2 * n, n) // (n + 1)
    assert g[2 * n] == formula, "递推与卡特兰公式不一致"
    print(g[2 * n])


main()
