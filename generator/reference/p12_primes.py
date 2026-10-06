"""p12 素数：输出第 n 个素数，以及 n 以内的素数个数（两个数一行）。
用埃氏筛：从 2 开始，把每个素数的倍数划掉。筛一次就能同时回答两个问题。
"""
import sys
from math import isqrt, log


def sieve(limit):
    """返回 2..limit 的全部素数（ bytearray 标记合数）。"""
    if limit < 2:
        return []
    is_comp = bytearray(limit + 1)
    for i in range(2, isqrt(limit) + 1):
        if not is_comp[i]:
            # 注意要写入 1（合数），写 bytearray(n) 全是 0，等于什么都没划掉
            is_comp[i * i:limit + 1:i] = b"\x01" * len(range(i * i, limit + 1, i))
    return [x for x in range(2, limit + 1) if not is_comp[x]]


def solve(n):
    # 先估一个够用的上界（第 6 个素数以后 p_k < k(ln k + ln ln k)），不够就翻倍再筛
    limit = 20 if n < 6 else int(n * (log(n) + log(log(n)))) + 10
    while True:
        ps = sieve(limit)
        if len(ps) >= n:
            break
        limit *= 2
    cnt_le_n = sum(1 for p in ps if p <= n)
    return ps[n - 1], cnt_le_n


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    nth, cnt = solve(int(data[0]))
    print(nth, cnt)


main()
