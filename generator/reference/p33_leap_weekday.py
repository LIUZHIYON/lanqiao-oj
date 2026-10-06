"""p33 闰年与星期：读入 y m d，输出「闰/平」和该日是周几（周一~周日）。
练的语法点：闰年判断表达式 + datetime 取星期（weekday() 里 0 是周一）。
"""
import datetime
import sys

WEEK = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or y % 400 == 0


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    y, m, d = int(data[0]), int(data[1]), int(data[2])
    leap = "闰" if is_leap(y) else "平"
    weekday = WEEK[datetime.date(y, m, d).weekday()]
    print(leap, weekday)


main()
