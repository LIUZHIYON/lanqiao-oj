"""p34 字符分类统计：一行文本，输出 字母数 数字数 其它字符数。
练的语法点：isalpha() / isdigit()。注意 isalpha() 对汉字也返回 True，
所以本题的「字母」限定为 A-Z 和 a-z，用 isascii() 卡住，汉字算其它字符。
"""
import sys


def main():
    text = sys.stdin.read()
    if text.endswith("\n"):
        text = text[:-1]            # 只去掉行末那一个换行，行里的空格要留着数
    alpha = digit = other = 0
    for c in text:
        if c.isdigit():
            digit += 1
        elif c.isascii() and c.isalpha():
            alpha += 1
        else:
            other += 1
    print(alpha, digit, other)


main()
