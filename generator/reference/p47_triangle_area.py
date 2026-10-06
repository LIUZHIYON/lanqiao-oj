"""p47 三角形判定与面积：读入三条边，能构成三角形输出 yes 和面积（保留 2 位），否则输出 no。
判定：三边排序后只要最短两条之和严格大于最长那条就行。
面积用海伦公式：s=(a+b+c)/2，area = sqrt(s(s-a)(s-b)(s-c))。
"""
import math
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    sides = sorted(float(x) for x in data[:3])
    a, b, c = sides
    if a + b > c:
        s = (a + b + c) / 2
        area = math.sqrt(max(0.0, s * (s - a) * (s - b) * (s - c)))
        print("yes {:.2f}".format(area))
    else:
        print("no")


main()
