"""p63 上台阶：n 级台阶，每步跨 1 级或 2 级，问一共有多少种走法。
线性 DP 最小的样子：把走法按"最后一步跨了几级"分成两类，
一类是最后跨 1 级（前面走掉 i-1 级，有 f[i-1] 种），一类是最后跨 2 级（有 f[i-2] 种），
两类不重不漏，所以 f[i] = f[i-1] + f[i-2]。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    f = [0] * (n + 2)             # 多开两格，n = 1 时也不会越界
    f[1] = 1                      # 1 级：只能跨 1 步
    f[2] = 2                      # 2 级：1+1 或者一次跨 2 级
    for i in range(3, n + 1):
        f[i] = f[i - 1] + f[i - 2]
    print(f[n])


main()
