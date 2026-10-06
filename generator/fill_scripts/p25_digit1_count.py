"""p25 填空：把 1~2026 依次写出来，一共用掉了多少个数字 1（22 里有 0 个，111 里有 3 个）。
做法 A：逐个数字符串里数 1 的个数。
做法 B：按数位统计公式，一位一位算 1 出现多少次。
"""

LIMIT = 2026


def count_digit_bruteforce(n, d=1):
    return sum(str(x).count(str(d)) for x in range(1, n + 1))


def count_digit_by_position(n, d=1):
    """统计 1..n 中数字 d（d 不为 0）出现的总次数。"""
    total, factor = 0, 1
    while n // factor:
        high = n // (factor * 10)
        cur = (n // factor) % 10
        low = n % factor
        if cur > d:
            total += (high + 1) * factor
        elif cur == d:
            total += high * factor + low + 1
        else:
            total += high * factor
        factor *= 10
    return total


a = count_digit_bruteforce(LIMIT, 1)
b = count_digit_by_position(LIMIT, 1)
assert a == b, (a, b)
for small in (9, 99, 500, 1325):
    for d in (1, 3, 7, 9):
        assert count_digit_by_position(small, d) == count_digit_bruteforce(small, d), (small, d)
print(a)
