'''a = input('Введи:').strip()
a1 = a.replace('[', '').replace(']', '').split(',')
a2 = [float(x.strip()) for x in a1 if x.strip()]'''

import ast

a1 = input("Введите: ")
a2 = ast.literal_eval(a1)

def frmt(x):
    return int(x) if x.is_integer() else x

def unique_sorted(n):
    s = sorted(set(n))
    d = []
    for i in range(len(s)):
       d.append(frmt(s[i]))
    return d
       
    
print(unique_sorted(a2))
    
