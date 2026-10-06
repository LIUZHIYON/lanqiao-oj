"""p11 最大子段和：选出连续的一段（至少含一个数），使和最大。
Kadane：cur = 以当前数结尾的最大子段和 = max(x, cur + x)，要么另起炉灶要么接着前面。
"""
import sys


def max_subarray(nums):
    cur = ans = nums[0]
    for x in nums[1:]:
        cur = x if cur < 0 else cur + x
        if cur > ans:
            ans = cur
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    nums = [int(x) for x in data[1:1 + n]]
    print(max_subarray(nums))


main()
