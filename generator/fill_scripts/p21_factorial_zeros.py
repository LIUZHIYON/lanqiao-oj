"""p21 填空：2022! 末尾有多少个 0。
一个 0 来自一对 2 和 5，而 2 比 5 多得多，所以只要数 2022! 里质因子 5 的个数：
2022//5 + 2022//25 + 2022//125 + 2022//625。再把 2022! 真算出来数尾巴验证。
"""
import math
import sys

sys.set_int_max_str_digits(0)

N = 2022


def legendre(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


by_formula = legendre(N, 5)
text = str(math.factorial(N))
real = len(text) - len(text.rstrip('0'))
assert by_formula == real, (by_formula, real)
print(real)
