import ast

r = input("Введите: ")
mat = ast.literal_eval(r)

def flatten(mat):
    result = []
    for r in mat:
        if not isinstance(r, (list, tuple)):
            raise TypeError
        result.extend(r)
    return result

try:
    print(flatten(mat))
except TypeError as e:
    print(f"TypeError: {e}")
    

