"""p28 四则运算套餐：一行读入两个正整数 a、b，输出和 差 积 整除商 余数。
练的语法点：+ - * // %，注意 // 是向下取整的整除，% 是取余。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    a, b = int(data[0]), int(data[1])
    print(a + b, a - b, a * b, a // b, a % b)


main()
