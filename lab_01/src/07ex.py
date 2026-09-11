f = open('lab_01/src/07ex.txt').readline()
frst = None
scnd = None

for i in range(len(f)):
    if frst is None and f[i].isupper():
        frst = i
    if scnd is None and f[i].isdigit():
        scnd = i + 1
        break
    
s = scnd - frst
i = frst
slovo = ''
while i < len(f) and f[i] != '.':
    slovo += f[i]
    i += s
    
        
print(slovo + '.')