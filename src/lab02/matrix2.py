import ast

r = input("Введите матрицу: ")
mat = ast.literal_eval(r)

def r_sum(mat):
    if mat and any(len(r) != len(mat[0]) for r in mat):
        raise ValueError("рваная матрица")
    return [sum(r) for r in mat]

try:
    print(r_sum(mat))
except ValueError as e:
    print(f"ValueError: рваная матрица ")