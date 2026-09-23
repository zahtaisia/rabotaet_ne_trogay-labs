def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Находит минимальное и максимальное значения в списке чисел.

    Args:
        nums (list[float | int]): Список чисел (int и/или float),
            для которых нужно найти минимум и максимум.

    Returns:
        tuple[float | int, float | int]: Кортеж вида (минимум, максимум).

    Raises:
        ValueError: Если список nums пустой."""
        
    if not (len(nums)):
        raise ValueError ('пустая строка')
    else:
        mx = nums[0]
        mn = nums[0]
        for n in nums:
            if n > mx:
                mx = n
            if n < mn:
                mn = n
        return mn, mx
    
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """
    Возвращает отсортированный список уникальных чисел из nums.

    Args:
        nums (list[float | int]): Список чисел (int и/или float).
            Внимание: список будет изменён (очищен) в процессе работы функции.

    Returns:
        list[float | int]: Отсортированный по возрастанию список
            уникальных значений из nums."""
    ans = []
    while len(nums) > 0:
        mn = nums[0]
        for n in nums:
            if n < mn and n not in ans:
                mn = n
        ans.append(mn)
        while mn in nums:
            nums.remove(mn)
    return ans
    
    
def flatten(mat: list[list | tuple]) -> list:
    """
    Разворачивает список списков/кортежей в один плоский список.

    Args:
        mat (list[list | tuple]): Список, элементами которого являются
            списки или кортежи, подлежащие объединению в один список.

    Returns:
        list: Плоский список, полученный последовательным объединением
            всех элементов mat.

    Raises:
        ValueError: Если mat — пустой список.
        TypeError: Если хотя бы один элемент mat не является
            списком или кортежем."""
    if not len(mat):
        raise ValueError ('пустая строка')
    else:
        pr = []
        for row in mat:
            if type(row) != list and type(row) != tuple:
                raise TypeError ('строка не является строкой строк матрицы')
            pr.extend(row)
        return pr
    
    
print('Тест кейсы:')
print(f'''
min_max

{min_max([3, -1, 5, 5, 0])}
{min_max([42])}
{min_max([-5, -2, -9])}
{min_max([1.5, 2, 2.0, -3.1])}
''')
# Тест кейс который выводит ошибку ValueError
# print(f'{min_max([])}')

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
''')

# Тест кейс который выводит ошибку TypeError
#print(f'{flatten([[1, 2], "ab"])}') 