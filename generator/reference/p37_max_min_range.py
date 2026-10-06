"""p37 最大最小极差：n 个整数，输出 最大值 最小值 极差。
练的语法点：打擂台——先拿第一个数当擂主，再逐个挑战。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:1 + n]]
    high = low = nums[0]
    for v in nums[1:]:
        if v > high:
            high = v
        if v < low:
            low = v
    print(high, low, high - low)


main()
