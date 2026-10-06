"""p16 填空：0~9 每种数字卡片各 2021 张，从 1 开始依次写正整数，最多能完整写到哪个数。
两种做法互验：A 一个个数往上加；B 按位统计 1..n 中数字 d 出现次数 + 二分。
"""


def simulate(limit):
    cnt = [0] * 10
    x = 1
    while True:
        for ch in str(x):
            d = ord(ch) - 48
            cnt[d] += 1
            if cnt[d] > limit:
                return x - 1
        x += 1


def digit_count_1_to_n(n, d):
    """1..n 中数字 d 出现多少次（按位算，d 为 0 时最高位不算）。"""
    total, factor = 0, 1
    while n // factor > 0:
        high = n // (factor * 10)
        cur = (n // factor) % 10
        low = n % factor
        if d == 0:
            if high == 0:
                factor *= 10
                continue
            total += (high - 1) * factor + (low + 1 if cur == 0 else 0)
        else:
            if cur > d:
                total += (high + 1) * factor
            elif cur == d:
                total += high * factor + low + 1
            else:
                total += high * factor
        factor *= 10
    return total


def by_binary_search(limit):
    lo, hi = 1, 10 ** 7
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if any(digit_count_1_to_n(mid, d) > limit for d in range(10)):
            hi = mid - 1
        else:
            lo = mid
    return lo


a = simulate(2021)
b = by_binary_search(2021)
assert a == b, (a, b)
assert all(digit_count_1_to_n(a, d) <= 2021 for d in range(10))
assert any(digit_count_1_to_n(a + 1, d) > 2021 for d in range(10))
print(a)
