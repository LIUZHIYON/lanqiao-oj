"""p31 BMI 判定：读入身高（米）和体重（公斤），输出偏瘦 / 正常 / 偏胖 / 肥胖。
练的语法点：if-elif-else 的区间划分（边界只写一次）与浮点数运算。
"""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    height = float(data[0])
    weight = float(data[1])
    bmi = weight / (height * height)
    if bmi < 18.5:
        print("偏瘦")
    elif bmi < 24:
        print("正常")
    elif bmi < 28:
        print("偏胖")
    else:
        print("肥胖")


main()
