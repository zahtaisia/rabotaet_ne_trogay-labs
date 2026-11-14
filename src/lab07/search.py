"""ЛР7. Поиск. Не нашли: -1 (поиск по индексу) или None (Two Sum)."""

from __future__ import annotations


def linear_search(nums: list[int], x: int) -> int:
    """Индекс первого вхождения x или -1. O(n).

    Args:
        nums: Список чисел (любой порядок).
        x: Искомое значение.

    Returns:
        Индекс первого вхождения или -1.

    linear_search([4, 2, 7, 2], 2) -> 1
    linear_search([4, 2, 7, 2], 9) -> -1
    linear_search([], 1) -> -1
    """
    for i, value in enumerate(nums):
        if value == x:
            return i
    return -1


def binary_search(sorted_nums: list[int], x: int) -> int:
    """Индекс x в списке, отсортированном по возрастанию, или -1. O(log n).

    На неотсортированном списке результат не определён.
    Инвариант: если x есть, он лежит между lo и hi включительно.

    Args:
        sorted_nums: Список, отсортированный по возрастанию.
        x: Искомое значение.

    Returns:
        Индекс любого вхождения x или -1.

    binary_search([1, 3, 5, 7], 5) -> 2
    binary_search([1, 3, 5, 7], 4) -> -1
    binary_search([5], 5) -> 0
    binary_search([], 5) -> -1
    """
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        if sorted_nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_sum_brute(nums: list[int], target: int) -> tuple[int, int] | None:
    """Перебор пар, O(n^2).

    Args:
        nums: Список чисел.
        target: Нужная сумма двух элементов.

    Returns:
        Пара индексов (i, j), i < j, nums[i] + nums[j] == target, или None.

    two_sum_brute([2, 7, 11, 15], 9) -> (0, 1)
    two_sum_brute([1, 2], 10) -> None
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums: list[int], target: int) -> tuple[int, int] | None:
    """То же, что two_sum_brute, но за один проход со словарём. O(n).

    Args:
        nums: Список чисел.
        target: Нужная сумма двух элементов.

    Returns:
        Пара индексов (i, j), i < j (при нескольких ответах - любая), или None.
    """
    seen = {}  # значение -> индекс
    for j, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], j)
        seen[x] = j
    return None