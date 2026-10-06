"""p53 区间和查询：数组固定、询问很多，先花 O(n) 算前缀和，
每次询问 [l, r] 就是 pre[r] - pre[l-1]，一次 O(1)。
前缀和下标多留一格（pre[0] = 0），就不用特判 l = 1。
询问很少时拿直接相加核对一遍。
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
    assert pre[n] == sum(a), "前缀和结尾没对上总和"

    out = []
    pos = 2 + n
    check = q <= 20 and n <= 3000             # 询问少时逐段直接加，核对用
    for _ in range(q):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        v = pre[r] - pre[l - 1]
        if check:
            assert v == sum(a[l - 1:r]), "前缀和与直接相加不一致"
        out.append(str(v))
    sys.stdout.write("\n".join(out) + "\n")


main()
