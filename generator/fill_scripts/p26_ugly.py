"""p26 填空：丑数指只含质因子 2、3、5 的正整数，把丑数从小到大排（1 算第 1 个），
求第 1500 个。
做法 A：三指针 DP，dp[i] = min(dp[p2]*2, dp[p3]*3, dp[p5]*5)，谁贡献了最小值谁前进。
做法 B：小根堆不断弹出最小值并把 x*2、x*3、x*5 入堆（用 set 去重）。
做法 C：把 A 的答案拿出来做一次"除尽 2、3、5 后是否剩 1"的验证。
"""
import heapq

N = 1500


def nth_ugly_dp(n):
    dp = [1] * n
    p2 = p3 = p5 = 0
    for i in range(1, n):
        dp[i] = min(dp[p2] * 2, dp[p3] * 3, dp[p5] * 5)
        if dp[i] == dp[p2] * 2:
            p2 += 1
        if dp[i] == dp[p3] * 3:
            p3 += 1
        if dp[i] == dp[p5] * 5:
            p5 += 1                        # 三个都是 if，用 elif 会漏掉重复值
    return dp[n - 1], dp


def nth_ugly_heap(n):
    seen = {1}
    heap = [1]
    val = 1
    for _ in range(n):
        val = heapq.heappop(heap)
        for p in (2, 3, 5):
            nv = val * p
            if nv not in seen:
                seen.add(nv)
                heapq.heappush(heap, nv)
    return val


def is_ugly(x):
    for p in (2, 3, 5):
        while x % p == 0:
            x //= p
    return x == 1


by_dp, seq = nth_ugly_dp(N)
by_heap = nth_ugly_heap(N)
assert by_dp == by_heap, (by_dp, by_heap)
assert all(is_ugly(v) for v in seq)
assert seq == sorted(set(seq))
print(by_dp)
