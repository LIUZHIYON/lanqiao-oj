"""p06 拼数：把 n 个数字串首尾相接，拼出尽量大的数。
按字典序从大到小排是错的（32 和 321）；正确比较规则是 a 排在 b 前面 <=> a+b > b+a。
functools.cmp_to_key 把比较函数变成 sort 能用的 key。
"""
import sys
from functools import cmp_to_key


def largest_concat(strs):
    def cmp(a, b):
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0
    return ''.join(sorted(strs, key=cmp_to_key(cmp)))


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    strs = data[1:1 + n]
    print(largest_concat(strs))


main()
