"""p09 约数：输出 n 的约数个数、以及 n 的最大真约数（除 n 自己以外最大的约数）。
约数个数用质因数分解：n = p1^e1 * p2^e2 ... 时约数个数 = (e1+1)(e2+1)...
最大真约数 = n 除以 n 的最小质因子。
"""
import sys


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


def solve(n):
    fac = factorize(n)
    cnt = 1
    smallest = min(fac)
    for e in fac.values():
        cnt *= e + 1
    return cnt, n // smallest


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    cnt, big = solve(int(data[0]))
    print(cnt, big)


main()
