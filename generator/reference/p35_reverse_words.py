"""p35 单词倒序：一行英文句子，把单词顺序反过来输出。
练的语法点：不带参数的 split() 会自动跳过多余空白，join 负责拼回去。
"""
import sys


def main():
    text = sys.stdin.read()
    if text.endswith("\n"):
        text = text[:-1]
    words = text.split()            # 不传参数：连续空白、首尾空白都会被自动处理
    sys.stdout.write(" ".join(reversed(words)) + "\n")


main()
