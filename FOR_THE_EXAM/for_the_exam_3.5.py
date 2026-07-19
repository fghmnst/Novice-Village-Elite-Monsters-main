#输出第n项斐波那契数列，但是最后使用三元运算符
n = int(input())
a, b = 1, 1
for _ in range(2, n):   # 循环 n-2 次
    a, b = b, a + b
print(b if n > 1 else a)  # n=1 时输出 a