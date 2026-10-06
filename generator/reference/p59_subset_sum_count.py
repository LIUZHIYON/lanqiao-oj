"""p59 凑数方案数：n 个数，每个最多选一次，问选出若干个使总和刚好等于 s 的方案数。
0-1 背包数方案：dp[j] = 和为 j 的方案数，dp[0] = 1（一个都不选）。
枚举每个数时内层要从大到小走，否则同一个数会被反复用。
方案数可能很大，Python 的整数不会溢出，直接原样输出。
中等规模用"只记出现过的和"的字典做法核对，极小规模再全枚举一遍。
"""
import sys


def count_by_dp(nums, s):
    dp = [0] * (s + 1)
    dp[0] = 1
    for a in nums:
        if a > s:                             # 单个数就超过目标，选它一定超
            continue
        for j in range(s, a - 1, -1):         # 逆序，保证每个数只用一次
            dp[j] += dp[j - a]
    return dp[s]


def count_by_dict(nums, s):
    cnt = {0: 1}
    for a in nums:
        add = {}
        for k, v in cnt.items():
            nk = k + a
            if nk <= s:
                add[nk] = add.get(nk, 0) + v
        for k, v in add.items():
            cnt[k] = cnt.get(k, 0) + v
    return cnt.get(s, 0)


def count_by_enum(nums, s):
    n = len(nums)
    hit = 0
    for mask in range(1 << n):
        tot = 0
        for i in range(n):
            if (mask >> i) & 1:
                tot += nums[i]
                if tot > s:
                    break
        if tot == s:
            hit += 1
    return hit


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, s = int(data[0]), int(data[1])
    nums = [int(x) for x in data[2:2 + n]]
    assert len(nums) == n, "数的个数和 n 对不上"
    ans = count_by_dp(nums, s)
    if n * (s + 1) <= 300000:
        assert ans == count_by_dict(nums, s), "数组递推与字典做法不一致"
    if n <= 14:                               # 全枚举是 2^n，只能核很小的
        assert ans == count_by_enum(nums, s), "递推与全枚举不一致"
    print(ans)


main()
