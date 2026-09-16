import ast

def transpose(mat):
    if mat and any(len(r) != len(mat[0]) for r in mat):
        raise ValueError("рваная матрица")
    return [list(col) for col in zip(*mat)]


r = input("Введите матрицу: ")
mat = ast.literal_eval(r)

try:
    print(transpose(mat))
except ValueError as e:
    print("ValueError: рваная матрица ")