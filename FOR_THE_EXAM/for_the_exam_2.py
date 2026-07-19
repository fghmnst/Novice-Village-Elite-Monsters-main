# 试编写程序，输入一个字符串，统计其中不同的字母字符和不同的数字字符的个数。
# 如输入：abcd1123@*
# 则显示：有4个不同的字母字符，3个不同的数字字符

string = input("输入一个字符串：")
set_letter =set()
set_digit =set()

for ch in string:
    
    if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
        set_letter.add(ch)

    if '0' <= ch <= '9':
        set_digit.add(ch)

print(f"有{len(set_letter)}个不同的字母字符，{len(set_digit)}个不同的数字字符")
