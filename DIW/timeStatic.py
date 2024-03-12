import datetime


def count_time(func):
    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()  # 程序开始时间
        func()
        over_time = datetime.datetime.now()   # 程序结束时间
        total_time = (over_time-start_time).total_seconds()
        print('%s 函数运行共计 %s秒' % (func.__name__, total_time))
    return int_time


@count_time
def main():
    print('>>>>开始计算函数运行时间')
    for i in range(1, 1000):# 可以是任意函数  ， 这里故意模拟函数的运行时间
        for j in range(i):
            print(j)


if __name__ == '__main__':
    main()