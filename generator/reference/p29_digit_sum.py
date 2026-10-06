"""p29 各位数字之和：第一行是组数 T，接下来 T 行各一个整数，输出每位数字相加的结果。
练的语法点：拆位（% 10 拿个位、// 10 去掉个位）。负号不计入，按绝对值拆。
"""
import sys


def digit_sum(n):
    n = abs(n)                      # 负号不参与求和
    total = 0
    while n > 0:
        total += n % 10             # 抠出最低位
        n //= 10                    # 去掉最低位
    return total                    # n 本来是 0 时循环不执行，正好返回 0


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        out.append(str(digit_sum(int(data[i]))))
    sys.stdout.write("\n".join(out) + "\n")


main()
