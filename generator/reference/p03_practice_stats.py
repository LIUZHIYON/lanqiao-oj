"""p03 刷题统计：从周一开始，工作日每天 a 题、周末每天 b 题，问第几天累计到 n。
一天一天模拟在 n 很大时会超时，所以先把整周（5a+2b 题）成批跳过，再逐天补。
"""
import sys


def day_when_reach(a, b, n):
    week = 5 * a + 2 * b            # 一整周做的题数
    full = n // week                # 可以整跳几周
    day = full * 7
    done = full * week
    while done < n:
        day += 1
        done += a if (day - 1) % 7 < 5 else b   # 前 5 天是周一到周五
    return day


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    a, b, n = int(data[0]), int(data[1]), int(data[2])
    print(day_when_reach(a, b, n))


main()
