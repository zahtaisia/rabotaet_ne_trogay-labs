import ast

raw = input("Введите матрицу: ")
mat = ast.literal_eval(raw)

def col_sums(mat):
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [sum(col) for col in zip(*mat)]

try:
    print(col_sums(mat))
except ValueError as e:
    print(f"ValueError: {e}")