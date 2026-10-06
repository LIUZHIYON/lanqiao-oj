"""p52 区间合并：给 n 个闭区间 [l, r]，把能并起来的并起来（端点相接也算重叠），
输出合并后的区间个数和覆盖的总长度（每个区间贡献 r - l，单点区间贡献 0）。
主做法：按左端点排序后一遍扫。
核对做法：把左右端点当事件扫一遍——同一坐标上先处理左端点再处理右端点，
          这样 [1,3] 和 [3,5] 在扫描里也接成一段，口径与合并算法一致。
"""
import sys


def merge_intervals(ivs):
    out = []
    for l, r in ivs:
        if out and l <= out[-1][1]:           # 与最后一段重叠或相接
            if r > out[-1][1]:
                out[-1][1] = r
        else:
            out.append([l, r])
    return out


def by_sweep(ivs):
    events = []
    for l, r in ivs:
        events.append((l, 0))                 # 0 = 左端点，排在同坐标的前面
        events.append((r, 1))                 # 1 = 右端点
    events.sort()
    depth = 0
    groups = 0
    length = 0
    prev = None
    for x, kind in events:
        if prev is not None and depth > 0 and x != prev:
            length += x - prev                # 这一段一直被盖着
        if kind == 0:
            if depth == 0:
                groups += 1
            depth += 1
        else:
            depth -= 1
        prev = x
    return groups, length


def solve(ivs):
    merged = merge_intervals(ivs)
    cnt = len(merged)
    total = sum(r - l for l, r in merged)
    s_cnt, s_len = by_sweep(ivs)
    assert (cnt, total) == (s_cnt, s_len), "排序合并与端点扫描不一致"
    return cnt, total


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    ivs = []
    pos = 1
    for _ in range(n):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        ivs.append((l, r))
    ivs.sort()                                # 按左端点排序，左端相同按右端
    cnt, total = solve(ivs)
    print(cnt, total)


main()
