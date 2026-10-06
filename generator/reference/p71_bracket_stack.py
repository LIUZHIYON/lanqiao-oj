"""p71 括号匹配（栈入门）：一行只含 ( 和 ) 的串，输出三样东西：
是否合法（合法 1，不合法 0）、扫描过程中达到的最大嵌套深度、
第一次配不上的位置（从左往右数，从 1 开始；全程不配错就输出 0）。
栈里存还没配上对的左括号的下标：遇到 ( 压栈，遇到 ) 就弹一个，
弹的时候栈是空的说明这个右括号没人配，最后栈没空说明还剩左括号。
"""
import sys


def main():
    s = sys.stdin.readline().strip()
    stack = []                        # 存左括号的位置（从 1 开始数）
    depth = 0
    bad_at = 0
    for i, ch in enumerate(s, start=1):
        if ch == "(":
            stack.append(i)
            if len(stack) > depth:
                depth = len(stack)    # 深度就是此刻栈里的左括号个数
        else:
            if stack:
                stack.pop()
            elif bad_at == 0:
                bad_at = i            # 第一次出现没得配的右括号
    ok = 1 if bad_at == 0 and not stack else 0
    print(ok, depth, bad_at)


main()
