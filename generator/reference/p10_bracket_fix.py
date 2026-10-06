"""p10 括号补全：给一串括号，求最少插入多少个能变成合法括号序列。
从左到右扫一遍：遇到 ( 就攒着；遇到 ) 若前面还有没配对的 ( 就抵消一个，
否则说明这里缺一个 (，记一次插入。最后还没配对的 ( 每个要补一个 )。
"""
import sys


def min_insert(s):
    waiting = 0     # 还没配对的左括号个数
    add = 0         # 不得不补的左括号个数
    for ch in s:
        if ch == '(':
            waiting += 1
        else:
            if waiting:
                waiting -= 1
            else:
                add += 1
    return add + waiting


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    print(min_insert(data[0]))


main()
