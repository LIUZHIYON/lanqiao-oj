"""p62 组合数取模：T 组询问，每组给 n、k，输出 C(n, k) mod 1000000007，k 大于 n 时输出 0。
预处理阶乘 fact[i] = i! mod p 和阶乘逆元 invfact[i] = (i!)^-1 mod p，
一次询问 O(1)：C(n,k) = fact[n] * invfact[k] * invfact[n-k]。
invfact[maxN] 用费马小定理 pow(fact[maxN], p-2, p) 求出来，再倒推 invfact[i-1] = invfact[i]*i。
核对：k 很小用连乘除逐个求逆元；n 不大直接用 math.comb 算精确值再取模。
"""
import sys
import math

MOD = 1000000007


def prepare(max_n):
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (max_n + 1)
    invfact[max_n] = pow(fact[max_n], MOD - 2, MOD)     # 费马小定理
    for i in range(max_n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD           # 倒推，少一次求幂
    return fact, invfact


def comb_mod(n, k, fact, invfact):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD


def comb_by_product(n, k):
    """C(n,k) = (n-k+1)*(n-k+2)*...*n / 1*2*...*k，每步用逆元代替除法。"""
    k = min(k, n - k)
    res = 1
    for i in range(1, k + 1):
        res = res * (n - k + i) % MOD * pow(i, MOD - 2, MOD) % MOD
    return res


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    qs = []
    pos = 1
    max_n = 0
    for _ in range(t):
        n, k = int(data[pos]), int(data[pos + 1])
        pos += 2
        qs.append((n, k))
        if n > max_n:
            max_n = n
    fact, invfact = prepare(max_n)

    out = []
    for n, k in qs:
        v = comb_mod(n, k, fact, invfact)
        if 0 <= k <= n and min(k, n - k) <= 60:         # 连乘除法核对
            assert v == comb_by_product(n, k), "阶乘逆元与连乘除不一致"
        if 0 <= k <= n and n <= 1000:                   # 精确值核对
            assert v == math.comb(n, k) % MOD, "阶乘逆元与精确组合数不一致"
        out.append(str(v))
    sys.stdout.write("\n".join(out) + "\n")


main()
