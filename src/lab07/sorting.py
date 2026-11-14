"""ЛР7. Сортировки. Возвращают НОВЫЙ список, исходный не меняют."""

from __future__ import annotations


def bubble_sort(nums: list[int]) -> list[int]:
    """Пузырёк, O(n^2). ★ Если за проход обменов не было - выходим.

    Args:
        nums: Исходный список (не меняется).

    Returns:
        Новый список, отсортированный по возрастанию.

    bubble_sort([3, 1, 2]) -> [1, 2, 3]
    bubble_sort([2, 2, 1]) -> [1, 2, 2]
    bubble_sort([]) -> []
    """
    a = list(nums)
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(nums: list[int]) -> list[int]:
    """Вставками, O(n^2): сдвигаем элемент влево, пока не встанет на место.

    Args:
        nums: Исходный список (не меняется).

    Returns:
        Новый отсортированный список.
    """
    a = list(nums)
    for i in range(1, len(a)):
        cur = a[i]
        j = i - 1
        while j >= 0 and a[j] > cur:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur
    return a


def selection_sort(nums: list[int]) -> list[int]:
    """Выбором, O(n^2): минимум оставшейся части ставим на границу.

    Args:
        nums: Исходный список (не меняется).

    Returns:
        Новый отсортированный список.
    """
    a = list(nums)
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def merge_sort(nums: list[int]) -> list[int]:
    """★ Слиянием снизу вверх, без рекурсии, O(n log n): отрезки длины 1, 2, 4, ...

    Args:
        nums: Исходный список (не меняется).

    Returns:
        Новый отсортированный список.
    """
    src = list(nums)
    n = len(src)
    width = 1
    while width < n:
        dst = []
        for lo in range(0, n, 2 * width):
            mid = lo + width if lo + width < n else n
            hi = lo + 2 * width if lo + 2 * width < n else n
            i, j = lo, mid
            while i < mid and j < hi:
                if src[i] <= src[j]:
                    dst.append(src[i])
                    i += 1
                else:
                    dst.append(src[j])
                    j += 1
            dst += src[i:mid] + src[j:hi]
        src = dst
        width *= 2
    return src


def counting_sort(nums: list[int], lo: int, hi: int) -> list[int]:
    """★ Подсчётом для целых из [lo, hi], O(n + (hi - lo)).

    Args:
        nums: Исходный список целых (не меняется).
        lo: Нижняя граница значений (включительно).
        hi: Верхняя граница значений (включительно).

    Returns:
        Новый отсортированный список.

    Raises:
        ValueError: Если значение вне диапазона [lo, hi].
    """
    counts = [0] * (hi - lo + 1)
    for x in nums:
        if x < lo or x > hi:
            raise ValueError(f"{x} вне диапазона [{lo}, {hi}]")
        counts[x - lo] += 1
    result = []
    for k, c in enumerate(counts):
        result += [lo + k] * c
    return result