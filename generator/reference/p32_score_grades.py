"""p32 成绩等级：n 个分数逐个评级（A/B/C/D），最后一行输出平均分保留两位小数。
练的语法点：多分支条件 + f-string 格式化输出（f"{x:.2f}"）。
"""
import sys


def grade(s):
    if s >= 90:
        return "A"
    if s >= 80:
        return "B"
    if s >= 60:
        return "C"
    return "D"


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    scores = [int(x) for x in data[1:1 + n]]
    lines = [grade(s) for s in scores]
    lines.append("{:.2f}".format(sum(scores) / n))
    sys.stdout.write("\n".join(lines) + "\n")


main()
