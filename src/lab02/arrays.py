def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not (len(nums)):
        raise ValueError ('пустая строка')
    return (min(nums), max(nums))

def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))

def flatten(mat: list[list | tuple]) -> list:
    vector = []
    for row in mat:
        if type(row) != list and type(row) != tuple:
            raise TypeError ('Передан не тот тип')
        vector.extend(row)
    return vector

print('Данные:')
print(f'''
min_max
{min_max([3, -1, 5, 5, 0])}
{min_max([42])}
{min_max([-5, -2, -9])}
{min_max([1.5, 2, 2.0, -3.1])}
''')

print(f'''
unique_sorted
{unique_sorted([3, 1, 2, 1, 3])}
{unique_sorted([])}
{unique_sorted([-1, -1, 0, 2, 2])}
{unique_sorted([1.0, 1, 2.5, 2.5, 0])}
''')

print(f'''
flatten
{flatten([[1, 2], [3, 4]])}
{flatten([[1, 2], (3, 4, 5)])}
{flatten([[1], [], [2, 3]])}
{flatten([[1, 2], "ab"])}
''')

