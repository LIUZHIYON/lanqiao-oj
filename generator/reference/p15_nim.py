"""p15 Nim 取石子：k 堆石子，每次从某一堆里至少取走一个，取光最后者胜。
结论：把每堆数量异或起来，结果是 0 则先手必败（输出 0），否则先手必胜（输出 1）。
"""
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    k = int(data[0])
    x = 0
    for i in range(1, k + 1):
        x ^= int(data[i])
    print(1 if x != 0 else 0)


main()
