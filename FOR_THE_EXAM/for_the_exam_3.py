#输出第n项斐波那契数列
n = int(input())  # 输入 n

if n == 1 or n == 2:
    print(1)
else:
    a, b = 1, 1          # 前两项
    for _ in range(3, n + 1):
        a, b = b, a + b  # 向后递推
    print(b)             # 此时 b 为第 n 项