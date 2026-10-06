"""p51 最长无重复字符子串：给一个字符串，输出最长的、内部没有重复字符的连续片段长度。
滑动窗口：right 往里扩，left 是窗口左边界。用 last[ch] 记住每个字符最后出现的位置，
一旦 last[ch] 落在窗口里，就把 left 跳到 last[ch] + 1（窗口只会往前走，不会往回退）。
串不长时用"每个位置往后扫"的暴力法核对。
"""
import sys


def longest_window(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        prev = last.get(ch, -1)
        if prev >= left:                      # 窗口里已经有 ch，左边界直接跳过它
            left = prev + 1
        last[ch] = right
        if right - left + 1 > best:
            best = right - left + 1
    return best


def by_brute(s):
    n = len(s)
    best = 0
    for i in range(n):
        seen = set()
        j = i
        while j < n and s[j] not in seen:
            seen.add(s[j])
            j += 1
        if j - i > best:
            best = j - i
    return best


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1]
    assert len(s) == n, "串长和 n 对不上"
    ans = longest_window(s)
    if n <= 500:                              # 暴力 O(n^2) 只在小时核对
        assert ans == by_brute(s), "滑动窗口与暴力不一致"
    print(ans)


main()
