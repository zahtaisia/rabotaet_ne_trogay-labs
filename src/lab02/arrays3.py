import ast

def flatten(mat):
    result = []
    for r in mat:
        if not isinstance(r, (list, tuple)):
            raise TypeError
        result.extend(r)
    return result


r = input("Введите: ")
mat = ast.literal_eval(r)

try:
    print(flatten(mat))
except TypeError as e:
    print(f"TypeError: строка не строка строк матрицы")
    

