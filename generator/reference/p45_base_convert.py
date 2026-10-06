"""p45 任意进制转换：十进制整数 n 转成 b 进制（2 到 16），负数带负号，10 以上用 A-F。
练的语法点：短除法——每次 n % b 拿到最低位，n //= b 往上走，最后反过来拼。
"""
import sys

DIGITS = "0123456789ABCDEF"


def to_base(n, b):
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    parts = []
    while n > 0:
        parts.append(DIGITS[n % b])
        n //= b
    if neg:
        parts.append("-")
    return "".join(reversed(parts))


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, b = int(data[0]), int(data[1])
    print(to_base(n, b))


main()
