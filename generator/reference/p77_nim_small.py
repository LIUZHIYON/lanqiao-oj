"""p77 取石子（Nim 入门）：k 堆石子，两人轮流，每次只能挑一堆、至少拿走一个，
拿走最后一颗的人赢，两人都绝顶聪明，问先手是不是必胜：是输出 1，不是输出 0。
结论：把每堆数量按位异或（Python 里的 ^），结果是 0 就先手必败，非 0 就先手必胜。
怕记不住结论就用递归硬算一遍所有局面核对（堆少、每堆少的时候才跑得完）。
"""
import sys
from functools import lru_cache


def brute_wins(piles):
    """当前行动的人是否必胜：枚举所有可能的拿法，只要有一种把对手逼进必败局面就行。"""

    @lru_cache(maxsize=None)
    def win(state):
        for i, v in enumerate(state):
            for take in range(1, v + 1):
                nxt = list(state)
                nxt[i] -= take
                if not win(tuple(nxt)):
                    return True
        return False                  # 一颗都拿不动，说明已经输了

    return win(tuple(piles))


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    k = int(data[0])
    piles = [int(x) for x in data[1:1 + k]]
    assert len(piles) == k, "堆数对不上"

    x = 0
    for v in piles:
        x ^= v
    ans = 1 if x != 0 else 0
    if k <= 3 and max(piles) <= 6:     # 局面总数 7^3 量级，递归还算得动
        assert ans == (1 if brute_wins(piles) else 0), "异或结论与递归硬算不一致"
    print(ans)


main()
