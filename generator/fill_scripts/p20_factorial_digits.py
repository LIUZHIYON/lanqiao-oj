"""p20 填空：2022! 写成十进制一共多少位。
先用 log10 估算，再把 2022! 真算出来数一遍字符串长度（Python 3.11 以后
默认禁止把超过约 4300 位的整数转成字符串，要先把限制关掉）。
"""
import math
import sys

sys.set_int_max_str_digits(0)

N = 2022
by_log = math.floor(math.lgamma(N + 1) / math.log(10)) + 1
by_sum = math.floor(sum(math.log10(i) for i in range(2, N + 1))) + 1
real = len(str(math.factorial(N)))
assert by_log == by_sum == real, (by_log, by_sum, real)
print(real)
