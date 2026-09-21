import ast

raw = input("Введите матрицу: ")
mat = ast.literal_eval(raw)

def row_sums(mat):
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [sum(row) for row in mat]

try:
    print(row_sums(mat))
except ValueError as e:
    print(f"ValueError: {e}")
    
