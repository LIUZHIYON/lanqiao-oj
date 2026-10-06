"""p36 回文判断：一行字符串，忽略大小写后判断是不是回文，输出 yes/no。
练的语法点：lower() 转小写 + 切片 [::-1] 反转，一行就能比完。
"""
import sys


def main():
    text = sys.stdin.read()
    if text.endswith("\n"):
        text = text[:-1]
    low = text.lower()
    print("yes" if low == low[::-1] else "no")


main()
