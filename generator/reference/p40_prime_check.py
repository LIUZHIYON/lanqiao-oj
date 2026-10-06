"""p40 素数判定：读入 n 个正整数，逐个输出 yes/no，最后输出素数个数。
练的语法点：isqrt 试除。只需试到平方根，先把 2 单独处理，再试奇数。
"""
import sys
from math import isqrt


def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    limit = isqrt(x)
    d = 3
    while d <= limit:
        if x % d == 0:
            return False
        d += 2
    return True


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:1 + n]]
    lines = []
    cnt = 0
    for v in nums:
        ok = is_prime(v)
        cnt += 1 if ok else 0
        lines.append("yes" if ok else "no")
    lines.append(str(cnt))
    sys.stdout.write("\n".join(lines) + "\n")


main()
