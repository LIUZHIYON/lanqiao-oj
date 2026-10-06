"""p46 水仙花数区间：读入 lo 和 hi，输出闭区间内所有三位水仙花数，逗号分隔，没有则输出 none。
水仙花数（三位）：各位数字的立方和等于它自己，例如 153 = 1^3 + 5^3 + 3^3。
练的语法点：枚举一个区间 + 拆位。
"""
import sys


def is_narcissistic(n):
    a = n // 100                  # 百位
    b = n // 10 % 10              # 十位
    c = n % 10                    # 个位
    return a * a * a + b * b * b + c * c * c == n


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    lo, hi = int(data[0]), int(data[1])
    out = []
    for n in range(max(lo, 100), min(hi, 999) + 1):
        if is_narcissistic(n):
            out.append(str(n))
    print(",".join(out) if out else "none")


main()
