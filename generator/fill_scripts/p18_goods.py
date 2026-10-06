"""p18 填空：L = 2022082731456292，统计满足 a*b*c = L 的有序三元组 (a,b,c) 有多少个。
方法 A：分解质因数后用隔板法，每个质因子的指数 ei 分给三个数 -> C(ei+2, 2)，整体相乘。
方法 B：枚举 L 的约数 a，对每个 a 数 b*c = L/a 的有序对数（即 L/a 的约数个数）再求和。
"""
from math import comb


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors_from_factors(n):
    ds = [1]
    for p, e in factorize(n).items():
        cur = []
        mul = 1
        for _ in range(e + 1):
            for d in ds:
                cur.append(d * mul)
            mul *= p
        ds = cur
    return sorted(ds)


def by_formula(n):
    ans = 1
    for e in factorize(n).values():
        ans *= comb(e + 2, 2)
    return ans


def by_divisor_sum(n):
    ds = divisors_from_factors(n)
    total = 0
    for a in ds:
        total += len(divisors_from_factors(n // a))
    return total


def brute(n):
    """只用于很小的数：直接三重枚举验证公式没写错。"""
    cnt = 0
    for a in range(1, n + 1):
        if n % a:
            continue
        for b in range(1, n // a + 1):
            if (n // a) % b == 0:
                cnt += 1
    return cnt


for small in (1, 2, 6, 12, 24, 30, 36, 120):
    assert by_formula(small) == by_divisor_sum(small) == brute(small), small
L = 2022082731456292
a = by_formula(L)
b = by_divisor_sum(L)
assert a == b, (a, b)
print(a)
