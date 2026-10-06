"""p02 时间显示：毫秒换成 H:MM:SS。
小时不补零，分钟和秒补零到两位。
"""
import sys


def fmt(t_ms):
    total = t_ms // 1000            # 先化成整秒，多余的毫秒直接丢掉
    h = total // 3600
    m = total % 3600 // 60
    s = total % 60
    return f"{h}:{m:02d}:{s:02d}"


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    print(fmt(int(data[0])))


main()
