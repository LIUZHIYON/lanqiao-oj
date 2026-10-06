"""p01 年号字串：把编号换成 Excel 列名那样的字母串。
读入一个正整数 n，输出对应字母串。
关键点：每一位是 1~26（A~Z），没有 0 这一位，所以每次取余前先 n -= 1。
"""
import sys


def to_column(n):
    res = []
    while n > 0:
        n -= 1                      # 把 1..26 压成 0..25
        res.append(chr(ord('A') + n % 26))
        n //= 26
    return ''.join(reversed(res))


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    print(to_column(int(data[0])))


main()
