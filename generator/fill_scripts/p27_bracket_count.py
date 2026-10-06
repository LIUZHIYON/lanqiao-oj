"""p27 填空：长度正好是 16 的合法括号序列有多少个（左右各 8 个，任何前缀里左括号都不少于右括号）。
做法 A：卡特兰数递推 g[2n] = sum(g[2j] * g[2n-2-2j])。
做法 B：公式 C(2n, n) / (n + 1)。
做法 C：16 位只有 2^16 种，直接全枚举一遍验证。
"""
from itertools import product
from math import comb

N = 8          # 8 对括号，长度 16


def catalan_dp(n):
    g = [0] * (2 * n + 1)
    g[0] = 1
    for i in range(2, 2 * n + 1, 2):
        for j in range(0, i - 1, 2):
            g[i] += g[j] * g[i - 2 - j]
    return g[2 * n]


def catalan_formula(n):
    return comb(2 * n, n) // (n + 1)


def brute(n):
    cnt = 0
    for bits in product('()', repeat=2 * n):
        bal, ok = 0, True
        for b in bits:
            bal += 1 if b == '(' else -1
            if bal < 0:
                ok = False
                break
        if ok and bal == 0:
            cnt += 1
    return cnt


for k in range(1, N + 1):
    assert catalan_dp(k) == catalan_formula(k), k
for k in range(1, 5):                     # 长度 8 以内再全枚举核对一次
    assert catalan_dp(k) == brute(k), k
a, b = catalan_dp(N), catalan_formula(N)
assert a == b, (a, b)
print(a)
