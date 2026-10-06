"""p42 手写冒泡排序：n 个整数升序输出。
练的语法点：双重 for 循环 + 相邻比较交换，不许用 sort / sorted。
外层每走完一趟，最大的就冒到末尾了，所以内层是 n-1-i 次。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:            # 一趟没交换说明已经有序，提前收工
            break
    sys.stdout.write(" ".join(map(str, a)) + "\n")


main()
