"""p81 柱状图里最大的矩形（单调栈提高）：
n 根宽度为 1 的柱子，各自有高度，选一段连续的柱子，矩形高度只能到这一段里最矮的那根，
问面积最大能是多少。
栈里存下标，栈内对应的高度从底到顶严格上升。遇到一根比栈顶矮的柱子，
栈顶那根就"到顶了"：弹出它，以它的高度能往左右各扩多远由新的栈顶和当前下标决定，
面积 = 高度 * (右边界 - 左边界 - 1)。
数据只到八百根，所以再用枚举每个起点往右扩、一路记最小高度的 O(n^2) 写法核对。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    h = [int(x) for x in data[1:1 + n]]
    assert len(h) == n, "柱子根数和 n 对不上"

    padded = h + [0]                  # 末尾补一根 0，收尾时把栈全部清空
    stack = []
    best = 0
    for i, v in enumerate(padded):
        while stack and padded[stack[-1]] > v:
            top = stack.pop()
            height = padded[top]
            left = stack[-1] if stack else -1
            area = height * (i - left - 1)
            if area > best:
                best = area
        stack.append(i)

    slow = 0                          # 暴力：枚举左端点，往右扩时记最矮
    for l in range(n):
        low = h[l]
        for r in range(l, n):
            if h[r] < low:
                low = h[r]
            area = low * (r - l + 1)
            if area > slow:
                slow = area
    assert best == slow, "单调栈与枚举两端点不一致"

    print(best)


main()
