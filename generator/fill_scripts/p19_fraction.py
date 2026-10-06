"""p19 填空：分子、分母都是 1~2022 的整数，能组成多少个既约分数（分子分母互质）。
固定分母 b，与 b 互质且不超过 b 的分子有 phi(b) 个；先把 a<=b 的半平面数完，
再乘 2，最后减掉被数了两次的 (1,1)。小数据再用 gcd 双重循环验证。
"""
from math import gcd


def phi_table(n):
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:                      # i 是质数，用它更新所有倍数
            for j in range(i, n + 1, i):
                phi[j] = phi[j] // i * (i - 1)
    return phi


def by_phi(n):
    phi = phi_table(n)
    return 2 * sum(phi[1:]) - 1


def by_gcd_double(n):
    return sum(1 for a in range(1, n + 1) for b in range(1, n + 1) if gcd(a, b) == 1)


for small in (1, 2, 5, 10, 30, 100):
    assert by_phi(small) == by_gcd_double(small), small
print(by_phi(2022))
