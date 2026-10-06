"""p69 区间和（前缀和入门）：pre[i] 记前 i 个数之和，pre[0] = 0，
问 [l, r] 的和就是 pre[r] - pre[l-1]，一次 O(1)。
多留 pre[0] 这一格，l = 1 就不用特判。询问少的时候把那段直接加起来核一遍。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, q = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    assert len(a) == n, "数组长度和 n 对不上"

    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]

    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        v = pre[r] - pre[l - 1]
        assert v == sum(a[l - 1:r]), "前缀和与直接相加不一致"   # 这题数据小，每次核一遍
        out.append(str(v))
    sys.stdout.write("\n".join(out) + "\n")


main()
