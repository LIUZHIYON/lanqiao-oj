"""p72 右边第一个更大的数（单调栈入门）：
对每个位置输出它右边第一个比它大的数，没有就输出 -1。
栈里存"还没找到答案的那些数的下标"，栈内对应的值从底到顶单调不升。
新数进来时，只要它比栈顶那个数大，栈顶就找到答案了：弹栈、写答案、接着比。
每个下标进出栈各一次，总共 O(n)。数据小，所以再用逐个往右看的 O(n^2) 写法核对。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    assert len(a) == n, "个数和 n 对不上"

    ans = [-1] * n
    stack = []                        # 存下标
    for i in range(n):
        while stack and a[stack[-1]] < a[i]:
            ans[stack.pop()] = a[i]
        stack.append(i)

    slow = []                         # 暴力：从 i+1 往右找第一个更大的
    for i in range(n):
        found = -1
        for j in range(i + 1, n):
            if a[j] > a[i]:
                found = a[j]
                break
        slow.append(found)
    assert ans == slow, "单调栈与暴力往右扫不一致"

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


main()
