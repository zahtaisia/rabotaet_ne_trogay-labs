def transpose(mat: list[list[float | int]]) -> list[list]:
    """Транспонирует матрицу.

    Args:
        mat: матрица как список строк; все строки одной длины.

    Returns:
        Новая матрица, в которой строки и столбцы поменялись местами.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [list(col) for col in zip(*mat)]

def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Считает суммы по строкам.

    Args:
        mat: матрица как список строк; все строки одной длины.

    Returns:
        Список, где i-й элемент равен сумме i-й строки.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [sum(row) for row in mat]

def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Считает суммы по столбцам.

    Args:
        mat: матрица как список строк; все строки одной длины.

    Returns:
        Список, где j-й элемент равен сумме j-го столбца.

    Raises:
        ValueError: если строки матрицы разной длины.
    """
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [sum(col) for col in zip(*mat)]



print('Тест кейсы:')
print(f'''
transpose

{transpose([[1, 2, 3]])}
{transpose([[1], [2], [3]])}
{transpose([[1, 2], [3, 4]])}
{transpose([])}
''')

# Возвращает ошибку ValueError
# print(f'{transpose([[1, 2], [3]])}')


print(f'''
row_sums

{row_sums([[1, 2, 3], [4, 5, 6]])}
{row_sums([[-1, 1], [10, -10]])}
{row_sums([[0, 0], [0, 0]])}
''')

# Возвращает ошибку ValueError
# print(f'{row_sums([[1, 2], [3]])}')


print(f'''
col_sums

{col_sums([[1, 2, 3], [4, 5, 6]])}
{col_sums([[-1, 1], [10, -10]])}
{col_sums([[0, 0], [0, 0]])}
''')

# Возвращает ошибку ValueError
# print(f'{col_sums([[1, 2], [3]])}')