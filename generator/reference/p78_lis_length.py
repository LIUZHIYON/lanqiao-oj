"""p78 最长上升子序列（线性 DP 提高）：
一列数里挑出一个尽量长的子序列（下标递增、允许不连续），要求严格上升，输出它的长度。
dp[i] = 以第 i 个数结尾的最长上升子序列长度，
它等于所有 j < i 且 a[j] < a[i] 里最长的 dp[j] 再加 1，谁都不接时自己是 1。
O(n^2) 的两层循环，一千个数就是五十万次比较，Python 跑得动。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    assert len(a) == n, "个数和 n 对不上"

    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1

    ans = max(dp)

    # 另一条路：tails[t] = 长度为 t+1 的上升子序列结尾最小能是多少，二分找插入位置
    import bisect
    tails = []
    for v in a:
        p = bisect.bisect_left(tails, v)      # 严格上升用 bisect_left
        if p == len(tails):
            tails.append(v)
        else:
            tails[p] = v
    assert len(tails) == ans, "O(n^2) 递推与二分维护不一致"

    print(ans)


main()
