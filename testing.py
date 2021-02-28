list = [
    '1','2','3','\n',
    '4','5','6','\n',
    '7','8','9'
]

x=""
'''
while True:
    for i in range(len(list)):
        if i == 2 or i == 5:
            x += "\n".join(list[i-1, i])
        elif i == 8:
            break
        else:
            x += "".join(i-1, i)
'''
print("".join(list))