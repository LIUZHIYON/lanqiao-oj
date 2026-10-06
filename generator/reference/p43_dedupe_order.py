"""p43 去重保序：n 个整数，按第一次出现的顺序输出不重复的数。
练的语法点：set 判重是 O(1)，但 set 本身没有顺序，所以要边扫边把新数收进结果表。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    seen = set()
    out = []
    for i in range(1, 1 + n):
        v = int(data[i])
        if v not in seen:
            seen.add(v)
            out.append(str(v))
    sys.stdout.write(" ".join(out) + "\n")


main()
