"""p08 完全平方数：给 N，求最小正整数 x，使 N*x 是完全平方数。
把 N 分解质因数：N = p1^e1 * p2^e2 ...
指数是偶数的质因子已经配成对，指数是奇数的还差一个，把它们各补一次乘起来就是 x。
"""
import sys


def factorize(n):
    """返回 {质因子: 指数}，只依赖试除。"""
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2       # 2 以后只试奇数
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def min_x(n):
    res = 1
    for p, e in factorize(n).items():
        if e % 2 == 1:
            res *= p
    return res


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    print(min_x(int(data[0])))


main()
