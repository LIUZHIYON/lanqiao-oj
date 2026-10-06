"""p24 填空：1~2026 这些数里，含有数字 2 的数一共有多少个（22 只算一个数）。
做法 A：逐个把数变成字符串判断。
做法 B：用整除和取余一位一位看。
做法 C：反过来数"不含 2 的数"（按位计数原理），再用总数去减。
"""

LIMIT = 2026


def has_two_str(x):
    return '2' in str(x)


def has_two_div(x):
    while x:
        if x % 10 == 2:
            return True
        x //= 10
    return False


def by_position_count(n):
    """1..n 中至少有一位是 2 的数的个数：先数每一位都不是 2 的（不含前导零问题
    用"补成同样长度、允许前导零"的办法处理，再减掉全 0 的那一个）。"""
    s = str(n)
    # 长度比 s 短的数：每个位置可取除 2 外的 9 个数字，减掉全 0
    total_short = 0
    for length in range(1, len(s)):
        total_short += 8 * 9 ** (length - 1)          # 首位不能是 0 也不能是 2
    # 与 s 等长且不超过 s 的：逐位比较
    cnt = 0
    prefix_ok = True
    for i, ch in enumerate(s):
        d = int(ch)
        rest = len(s) - i - 1
        for nd in range(0 if i else 1, d):            # 本位取一个比 s 小的数字
            if nd == 2 or (i == 0 and nd == 0):
                continue
            cnt += 9 ** rest                          # 后面每位都能取非 2 的 9 个
        if d == 2:
            prefix_ok = False
            break
    if prefix_ok:
        cnt += 1                                      # s 本身也不含 2
    no_two = total_short + cnt
    return n - no_two


a = sum(1 for x in range(1, LIMIT + 1) if has_two_str(x))
b = sum(1 for x in range(1, LIMIT + 1) if has_two_div(x))
c = by_position_count(LIMIT)
assert a == b == c, (a, b, c)
for small in (9, 25, 130, 999, 1500):
    assert by_position_count(small) == sum(1 for x in range(1, small + 1) if has_two_str(x)), small
print(a)
