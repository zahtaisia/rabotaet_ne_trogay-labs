strk = input('Введите строку:')
frst = None
scnd = None

for i in range(len(strk)):
    if frst is None and strk[i].isupper():
        frst = i
    if scnd is None and strk[i].isdigit():
        scnd = i + 1
        break
    
s = scnd - frst
i = frst
slovo = ''
while i < len(strk) and strk[i] != '.':
    slovo += strk[i]
    i += s
    
        
print(slovo + '.')