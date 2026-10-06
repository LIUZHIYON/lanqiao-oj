"""p61 最长公共子序列：给两个串，输出它们公共子序列的最长长度。
子序列不要求连续（"abc" 里 "ac" 是子序列，但 "ca" 不是），所以是二维 DP：
dp[i][j] = 前 i 个 和 前 j 个 的 LCS 长度。
末字符相同 -> 左上角 + 1；不同 -> 上面和左边取大的。只依赖上一行，滚动两行就够。
串很短时用枚举全部子序列暴力核对，中等规模时再确认 lcs(a,b) 和 lcs(b,a) 相等。
"""
import sys


def lcs_len(a, b):
    m = len(b)
    prev = [0] * (m + 1)
    for ca in a:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if b[j - 1] == ca:
                cur[j] = prev[j - 1] + 1
            else:
                up = prev[j]
                left = cur[j - 1]
                cur[j] = up if up >= left else left
        prev = cur
    return prev[m]


def is_subseq(short, long):
    it = iter(long)
    return all(ch in it for ch in short)


def by_brute(a, b):
    """枚举 a 的所有子序列，能塞进 b 的最长的那个就是答案。"""
    n = len(a)
    best = 0
    for mask in range(1 << n):
        sub = "".join(a[i] for i in range(n) if (mask >> i) & 1)
        if len(sub) <= best or len(sub) > len(b):
            continue
        if is_subseq(sub, b):
            best = len(sub)
    return best


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    a, b = data[2], data[3]
    assert len(a) == n and len(b) == m, "串长和给定的 n、m 对不上"
    ans = lcs_len(a, b)
    if n * m <= 400000:                       # 再跑一遍代价不小，只在中等规模核对
        assert ans == lcs_len(b, a), "交换两个串结果应当不变"
    if min(n, m) <= 10:                       # 全枚举是 2 的幂次，只能核很短的
        short, long = (a, b) if n <= m else (b, a)
        assert ans == by_brute(short, long), "DP 与枚举子序列不一致"
    print(ans)


main()
