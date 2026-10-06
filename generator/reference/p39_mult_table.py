"""p39 九九乘法表：读入 n（不超过 9），输出前 n 行。
第 i 行有 i 个算式，依次是 1*i、2*i、……、i*i，算式之间一个空格。
练的语法点：嵌套循环 + 用 join 拼一行，避免行末多空格。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    lines = []
    for i in range(1, n + 1):
        parts = []
        for j in range(1, i + 1):
            parts.append("{}*{}={}".format(j, i, j * i))
        lines.append(" ".join(parts))
    sys.stdout.write("\n".join(lines) + "\n")


main()
