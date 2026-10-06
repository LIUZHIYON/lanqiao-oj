"""p30 秒数换算：把总秒数换成 天 时 分 秒 四个数。
练的语法点：连续整除与取余，先算大单位，再拿剩下的去算小单位。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    s = int(data[0])
    day = s // 86400
    rest = s % 86400
    hour = rest // 3600
    rest %= 3600
    minute = rest // 60
    second = rest % 60
    print(day, hour, minute, second)


main()
