"""p44 字符 Top-K：一行小写字母与数字组成的串，再给一个 k，
输出出现次数最多的 k 个字符，格式 字符:次数，空格分隔。
次数从多到少排；次数相同按字符本身从小到大排。
练的语法点：计数 + 把 (-次数, 字符) 当排序键，一次搞定两个条件。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    s, k = data[0], int(data[1])
    cnt = {}
    for c in s:
        cnt[c] = cnt.get(c, 0) + 1
    items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    out = ["{}:{}".format(c, t) for c, t in items[:k]]
    sys.stdout.write(" ".join(out) + "\n")


main()
