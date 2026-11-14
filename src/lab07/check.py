"""ЛР7. Проверка своих функций против эталона на случайных данных.

python -m src.lab07.check              - прогнать всё, напечатать OK: N проверок
python -m src.lab07.check --self-test  - проверить, что проверка ловит плохие функции
"""

import random
import sys

from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import (bubble_sort, counting_sort, insertion_sort,
                               merge_sort, selection_sort)

count = 0  # сколько проверок выполнено


def rand_list(lo=-100, hi=100, max_len=50):
    """Случайный список длиной 0..max_len, с повторами и отрицательными."""
    return [random.randint(lo, hi) for _ in range(random.randint(0, max_len))]


def check_sorting(fn, trials=100):
    """fn(nums) == sorted(nums), исходный список не изменён."""
    global count
    cases = [[], [5], [10, 9], [2, 2, 1]] + [rand_list() for _ in range(trials)]
    for nums in cases:
        copy = nums[:]
        assert fn(nums) == sorted(copy), f"{fn.__name__} ошиблась на {copy}"
        assert nums == copy, f"{fn.__name__} изменила исходный список {copy}"
        count += 1
    print(f"OK: {fn.__name__}, {len(cases)} проверок")


def check_binary(fn, a, x):
    """Если x есть в a - fn вернула его индекс, иначе -1."""
    global count
    i = fn(a, x)
    if x in a:
        assert i != -1 and a[i] == x, f"{fn.__name__}({a}, {x}) вернула {i}"
    else:
        assert i == -1, f"{fn.__name__}({a}, {x}) вернула {i}"
    count += 1


def check_search():
    """linear_search против list.index, binary_search - по свойству ответа."""
    global count
    assert binary_search([], 5) == -1 and binary_search([5], 5) == 0
    assert binary_search([1, 3], 2) == -1
    for _ in range(100):
        nums = rand_list(-20, 20)
        x = random.randint(-25, 25)
        try:
            expected = nums.index(x)
        except ValueError:  # list.index бросает ValueError, у нас это -1
            expected = -1
        assert linear_search(nums, x) == expected, f"linear_search({nums}, {x})"
        count += 1
        a = sorted(nums)
        for y in [x] + a[:1] + a[-1:]:  # случайный x, первый и последний элементы
            check_binary(binary_search, a, y)
    print("OK: linear_search + binary_search")


def check_two_sum(trials=100):
    """Оба способа: пара с нужной суммой (i < j) или оба None."""
    global count
    for k in range(trials):
        nums = rand_list(-20, 20, 30)
        target = random.randint(-45, 45)
        if k % 2 == 0 and len(nums) >= 2:  # в половине случаев ответ точно есть
            i, j = random.sample(range(len(nums)), 2)
            target = nums[i] + nums[j]
        a, b = two_sum_brute(nums, target), two_sum_fast(nums, target)
        assert (a is None) == (b is None), f"{nums}, {target}: {a} и {b}"
        for p in (a, b):
            if p is not None:
                assert p[0] < p[1] and nums[p[0]] + nums[p[1]] == target, \
                    f"{nums}, {target}: неверная пара {p}"
        count += 1
    print("OK: two_sum_brute + two_sum_fast")


def run_all():
    """Все проверки, итог - OK: N проверок."""
    global count
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort, merge_sort):
        check_sorting(fn)
    for _ in range(100):  # ★ counting_sort
        nums = rand_list(-30, 30)
        assert counting_sort(nums, -30, 30) == sorted(nums), f"counting_sort на {nums}"
        count += 1
    print("OK: counting_sort, 100 проверок")
    check_search()
    check_two_sum()
    print(f"OK: {count} проверок")


def bad_key_str(nums):
    """Плохая сортировка: числа как строки."""
    return sorted(nums, key=str)


def bad_in_place(nums):
    """Плохая сортировка: меняет исходный список."""
    nums.sort()
    return nums


def bad_binary(a, x):
    """Плохой бинарный поиск: lo < hi вместо lo <= hi."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        elif a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def self_test():
    """Каждая плохая функция должна упасть на проверке."""
    random.seed(42)
    for fn in (bad_key_str, bad_in_place):
        try:
            check_sorting(fn)
        except AssertionError as e:
            print("поймали:", e)
    try:
        for _ in range(100):
            check_binary(bad_binary, sorted(rand_list(-20, 20)), random.randint(-25, 25))
    except AssertionError as e:
        print("поймали:", str(e)[:70])


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        run_all()