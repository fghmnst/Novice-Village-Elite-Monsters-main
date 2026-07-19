# 输入两个整数表示年份和月份，打印这个月的天数，考虑月份输入错误的情况
try:
    year = int(input("输入一个年份: "))
    month = int(input("输入一个月份: "))

    if month < 1 or month > 12:
        print("请输入1至12范围内的整数！")

    else:
        if month in (1, 3, 5, 7, 8, 10, 12):
            days = 31

        elif month in (4, 6, 9, 11):
            days = 30

        else:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                days = 29
            else:
                days = 28

        print(f"{year}年{month}月有{days}天")

except ValueError:
    print("输入无效，请输入整数！")