"""p48 既约分数计数：分子、分母都从 1..n 里取，问有多少个有序对 (a, b) 互质。
方法一：欧拉函数筛。按 max(a, b) = k 分层，k 这一层新添 2*phi(k) 对，
        所以答案 = 2 * (phi(1) + ... + phi(n)) - 1（(1,1) 多算了一次）。
方法二：莫比乌斯容斥。答案 = Σ mu(d) * (n // d) ** 2。
两种筛法互相核对；n 很小时再用 gcd 双循环暴力验一遍。
"""
import sys
from math import gcd


def phi_sieve(n):
    """埃氏筛风格的欧拉函数：遇到素数 i 就把 i 的倍数的 phi 缩一次。"""
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:                       # phi[i] 没被动过 -> i 是素数
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi


def mobius_sieve(n):
    """线性筛顺带得到莫比乌斯函数：质因子有重复记 0，否则 (-1) 的个数次方。"""
    mu = [0] * (n + 1)
    mu[1] = 1
    primes = []
    comp = bytearray(n + 1)
    for i in range(2, n + 1):
        if not comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            comp[i * p] = 1
            if i % p == 0:                    # p 重复出现，mu 直接是 0
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def count_by_phi(n):
    return 2 * sum(phi_sieve(n)[1:]) - 1


def count_by_mu(n):
    mu = mobius_sieve(n)
    return sum(mu[d] * (n // d) * (n // d) for d in range(1, n + 1))


def count_by_gcd(n):
    cnt = 0
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            if gcd(a, b) == 1:
                cnt += 1
    return cnt


def solve(n):
    by_phi = count_by_phi(n)
    by_mu = count_by_mu(n)
    assert by_phi == by_mu, "欧拉函数与莫比乌斯两种数法不一致"
    if n <= 200:                              # 小规模用暴力双循环再核一次
        assert count_by_gcd(n) == by_phi, "暴力 gcd 与筛法不一致"
    return by_phi


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    print(solve(int(data[0])))


main()
