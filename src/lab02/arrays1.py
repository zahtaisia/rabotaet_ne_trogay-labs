import ast

a1 = input("Введите: ")
a2 = ast.literal_eval(a1)

"""def frmt(x):
    return int(x) if x.is_integer() else x"""

def min_max(n):
    if n:
        return (min(n)), (max(n))
    return 'ValueError'
    
print(min_max(a2))
