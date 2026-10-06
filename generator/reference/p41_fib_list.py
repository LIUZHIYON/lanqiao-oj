"""p41 斐波那契前 n 项：读入 n（不超过 90），一行输出前 n 项，空格分隔。
规定第 1 项、第 2 项都是 1。练的语法点：递推（滚动两个变量）与 Python 大整数。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a, b = 1, 1                    # a 是当前项，b 是下一项
    out = []
    for _ in range(n):
        out.append(str(a))
        a, b = b, a + b
    sys.stdout.write(" ".join(out) + "\n")


main()
