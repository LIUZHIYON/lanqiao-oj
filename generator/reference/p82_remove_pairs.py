"""p82 彩球消消乐（栈提高）：
一行彩球，只要有一对相邻的颜色相同，这两个就一起消失，消失后左右接上继续消，
一直消到没有任何相邻相同为止，输出最后剩下的串（顺序不变）；全消光了输出 empty。
一遍扫描就够：栈里存还没消掉的球，来的新球和栈顶相同就把栈顶弹掉（一对没了），
不同就压栈。反复"整行扫一遍找一对消掉"的写法也能对，只是慢得多，
所以这里拿它当小数据的核对。
"""
import sys


def by_stack(s):
    stack = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()               # 和栈顶凑成一对，同归于尽
        else:
            stack.append(ch)
    return "".join(stack)


def by_naive(s):
    """一遍一遍整行扫，找到能消的相邻对就消掉，再从头扫。"""
    cur = s
    while True:
        out = []
        i = 0
        changed = False
        while i < len(cur):
            if i + 1 < len(cur) and cur[i] == cur[i + 1]:
                i += 2
                changed = True
            else:
                out.append(cur[i])
                i += 1
        cur = "".join(out)
        if not changed:
            return cur


def main():
    s = sys.stdin.readline().strip()
    ans = by_stack(s)
    if len(s) <= 600:                 # 串不长时再拿反复整行扫核一遍
        assert ans == by_naive(s), "栈的一遍扫描与反复整行扫不一致"
    print(ans if ans else "empty")


main()
