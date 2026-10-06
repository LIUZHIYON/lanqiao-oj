"""p38 计数筛选：n 个数里挑出大于等于 x 的，输出个数与它们的和。
练的语法点：循环里加条件的累加（计数 + 求和一起算）。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, x = int(data[0]), int(data[1])
    cnt = 0
    total = 0
    for i in range(2, 2 + n):
        v = int(data[i])
        if v >= x:
            cnt += 1
            total += v
    print(cnt, total)


main()
