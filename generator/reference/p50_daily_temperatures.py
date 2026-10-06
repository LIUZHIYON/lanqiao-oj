"""p50 每日温度：对每一天输出"还要等几天才出现更高的温度"，等不到输出 0。
单调栈：栈里存还没有答案的下标，栈内温度从底到顶单调不升。
新的一天比栈顶高，就把栈顶结算掉（等待天数 = 下标差），直到栈顶不再比它低，然后把今天压栈。
规模小的时候再用两层循环暴力核对一遍。
"""
import sys


def daily_temps(temps):
    n = len(temps)
    res = [0] * n
    stack = []                                # 存下标，对应的温度单调不升
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()                   # 今天 t 比栈顶那天高 -> 结算
            res[j] = i - j
        stack.append(i)
    return res


def by_brute(temps):
    n = len(temps)
    res = []
    for i in range(n):
        wait = 0
        for j in range(i + 1, n):
            if temps[j] > temps[i]:
                wait = j - i
                break
        res.append(wait)
    return res


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    temps = [int(x) for x in data[1:1 + n]]
    assert len(temps) == n, "温度个数和 n 对不上"
    ans = daily_temps(temps)
    if n <= 400:                              # 小数据用 O(n^2) 暴力核一遍
        assert ans == by_brute(temps), "单调栈与暴力不一致"
    sys.stdout.write(" ".join(map(str, ans)) + "\n")


main()
