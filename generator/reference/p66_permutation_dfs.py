"""p66 全排列（回溯入门）：把 1 到 n 排成一排，输出所有排法。
回溯三件事：做选择（标记用过、放进 path）、递归往下走、撤销选择。
for 循环从小到大试，所以吐出来的顺序正好就是字典序。
"""
import itertools
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    used = [False] * (n + 1)      # used[x] 表示数字 x 已经在排好的部分里
    path = []                     # 当前排到一半的序列
    out = []

    def dfs():
        if len(path) == n:        # 每个数字都用上了，收集一个答案
            out.append(" ".join(map(str, path)))
            return
        for x in range(1, n + 1):
            if used[x]:
                continue
            used[x] = True
            path.append(x)
            dfs()
            path.pop()            # 撤销：回来时状态必须和进去之前一模一样
            used[x] = False

    dfs()
    # 拿标准库的全排列核对一遍，确认没有漏、没有重、顺序也对
    expect = [" ".join(map(str, t)) for t in itertools.permutations(range(1, n + 1))]
    assert out == expect, "回溯结果与 itertools 不一致"

    print(len(out))
    sys.stdout.write("\n".join(out) + "\n")


main()
