"""ЛР7. Бенчмарк: поиск, сортировки, Two Sum.

Запуск из корня репозитория:
    python -m src.lab07.bench

Правила честного замера:
    * данные читаются из data/samples/lab07/numbers_{n}.csv (если файлов нет -
      генерируются с random.seed(42)) и подаются ВСЕМ алгоритмам одни и те же;
    * замер - timeit; для быстрых операций number > 1 и результат делится;
    * каждый замер идёт в отдельном процессе с лимитом TIME_LIMIT секунд:
      если не уложился - в таблице "> 60", это и есть результат
      (квадратичная сортировка на 10^5 - ~10^10 шагов, около получаса).

Результат: таблица в консоль и data/lab07/bench.csv (task,n,impl,seconds).
"""

from __future__ import annotations

import csv
import multiprocessing
import random
import timeit
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import (
    binary_search,
    linear_search,
    two_sum_brute,
    two_sum_fast,
)
from src.lab07.sorting import (
    bubble_sort,
    counting_sort,
    insertion_sort,
    merge_sort,
    selection_sort,
)

SEED = 42
TIME_LIMIT = 60  # секунд на один замер
SAMPLES_DIR = Path("data/samples/lab07")
OUT_CSV = Path("data/lab07/bench.csv")
PLOT_PNG = Path("images/lab07/sort_times.png")
HEADER = ("task", "n", "impl", "seconds")
LIMIT_MARK = f">{TIME_LIMIT}"

SORT_SIZES = (1_000, 10_000, 100_000)
SEARCH_N = 100_000
SEARCH_QUERIES = 10_000
TWO_SUM_SIZES = (1_000, 10_000)
NARROW_SIZES = (100_000, 1_000_000)  # для counting_sort: значения 0..1000
NARROW_HI = 1000

OWN_SORTS = (
    ("bubble_sort", bubble_sort),
    ("insertion_sort", insertion_sort),
    ("selection_sort", selection_sort),
    ("merge_sort", merge_sort),
)


# --------------------------------------------------------------------------
# Данные
# --------------------------------------------------------------------------
def make_samples() -> None:
    """Создать data/samples/lab07/numbers_{n}.csv, если файла ещё нет."""
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    sizes = sorted(set(SORT_SIZES) | {SEARCH_N} | set(TWO_SUM_SIZES))
    for n in sizes:
        path = SAMPLES_DIR / f"numbers_{n}.csv"
        if path.exists():
            continue
        rng = random.Random(SEED)
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["value"])
            for _ in range(n):
                w.writerow([rng.randint(-1_000_000, 1_000_000)])


def read_numbers(path) -> list[int]:
    """Прочитать колонку value из CSV и сразу превратить строки в int."""
    with open(path, encoding="utf-8") as f:
        return [int(row["value"]) for row in csv.DictReader(f)]


def load(n: int) -> list[int]:
    """Данные размера n из data/samples/lab07."""
    return read_numbers(SAMPLES_DIR / f"numbers_{n}.csv")


# --------------------------------------------------------------------------
# Замер с лимитом времени
# --------------------------------------------------------------------------
def _worker(queue, fn, args, number) -> None:
    t = timeit.timeit(lambda: fn(*args), number=number) / number
    queue.put(t)


def timed(fn, args=(), number: int = 1, limit: int = TIME_LIMIT):
    """Среднее время одного вызова fn(*args) через timeit или None по лимиту.

    Замер идёт в отдельном процессе, чтобы можно было остановить слишком
    долгий вызов.

    Args:
        fn: Функция (на уровне модуля, чтобы её можно было передать процессу).
        args: Аргументы функции.
        number: Сколько раз вызвать внутри timeit (результат делится на number).
        limit: Лимит на весь замер, секунд.

    Returns:
        Секунды на один вызов или None, если уложиться в limit не удалось.
    """
    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=_worker, args=(queue, fn, args, number))
    proc.start()
    proc.join(limit)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return None
    return queue.get(timeout=5)


def run_queries(search_fn, haystack: list[int], queries: list[int]) -> int:
    """Выполнить все запросы поиска; возвращает число найденных."""
    found = 0
    for q in queries:
        if search_fn(haystack, q) != -1:
            found += 1
    return found


# --------------------------------------------------------------------------
# Серии замеров
# --------------------------------------------------------------------------
def bench_sorts(n: int) -> list[tuple]:
    """Сортировки на ОДНИХ И ТЕХ ЖЕ данных numbers_{n}.csv."""
    data = load(n)
    sorted_number = {1_000: 20, 10_000: 10}.get(n, 3)
    own_number = 5 if n <= 1_000 else 1
    rows = [("sort", n, "sorted", timed(sorted, (data,), sorted_number))]
    for name, fn in OWN_SORTS:
        rows.append(("sort", n, name, timed(fn, (data,), own_number)))
    return rows


def bench_search() -> list[tuple]:
    """Линейный против бинарного: 10 000 запросов к списку из 100 000.

    Запросы - случайные элементы списка (всегда найдутся). Для бинарного
    поиска время сортировки списка идёт отдельной строкой.
    """
    data = load(SEARCH_N)
    rng = random.Random(SEED)
    queries = [rng.choice(data) for _ in range(SEARCH_QUERIES)]
    sorted_data = sorted(data)
    return [
        ("search", SEARCH_N, "linear_search",
         timed(run_queries, (linear_search, data, queries))),
        ("search", SEARCH_N, "binary_search",
         timed(run_queries, (binary_search, sorted_data, queries))),
        ("search", SEARCH_N, "sorted_for_binary", timed(sorted, (data,), 3)),
    ]


def bench_two_sum() -> list[tuple]:
    """Two Sum: target гарантированно существует, ответ - в самом конце списка.

    В случайных данных сумм-совпадений много, и перебор находит пару почти
    сразу, не показывая n^2. Поэтому все числа делаем чётными, а последнее -
    нечётным: нечётная сумма получается только с участием последнего
    элемента, то есть единственный ответ - пара (n - 2, n - 1). Это худший
    случай и для перебора (~n^2/2 пар), и для словаря (полный проход).
    """
    rows = []
    for n in TWO_SUM_SIZES:
        data = [2 * v for v in load(n)]
        data[-1] += 1
        target = data[n - 2] + data[n - 1]
        rows.append(("two_sum", n, "two_sum_brute",
                     timed(two_sum_brute, (data, target))))
        rows.append(("two_sum", n, "two_sum_fast",
                     timed(two_sum_fast, (data, target), 20)))
    return rows


def bench_counting() -> list[tuple]:
    """★ Случай, где counting_sort обгоняет sorted: узкий диапазон значений."""
    rows = []
    for n in NARROW_SIZES:
        rng = random.Random(SEED)
        data = [rng.randint(0, NARROW_HI) for _ in range(n)]
        number = 3 if n <= 100_000 else 2
        rows.append(("sort_narrow", n, "sorted", timed(sorted, (data,), number)))
        rows.append(("sort_narrow", n, "counting_sort",
                     timed(counting_sort, (data, 0, NARROW_HI), number)))
    return rows


# --------------------------------------------------------------------------
# Вывод
# --------------------------------------------------------------------------
def fmt_seconds(value) -> str:
    """Секунды для таблицы: число или метка лимита."""
    return LIMIT_MARK if value is None else f"{value:.6f}"


def print_table(rows: list[tuple]) -> None:
    """Таблица с выравниванием (f-строки)."""
    print(f"{'task':<12}{'n':>10}  {'impl':<18}{'seconds':>12}")
    print("-" * 54)
    for task, n, impl, sec in rows:
        print(f"{task:<12}{n:>10}  {impl:<18}{fmt_seconds(sec):>12}")


def save_csv(rows: list[tuple]) -> None:
    """Сохранить таблицу в data/lab07/bench.csv через write_csv из ЛР4."""
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out = [(t, n, impl, fmt_seconds(sec)) for t, n, impl, sec in rows]
    write_csv(out, OUT_CSV, header=HEADER)


def plot_sorts(csv_path=OUT_CSV, png_path=PLOT_PNG) -> bool:
    """★ График из bench.csv: время от n для всех сортировок, ось Y - log.

    Замеры «>60» рисуются крестиком на уровне лимита.

    Returns:
        True, если график сохранён; False, если нет matplotlib.
    """
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib не установлен - график пропущен (pip install matplotlib)")
        return False

    series: dict[str, list[tuple[int, float, bool]]] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["task"] != "sort":
                continue
            over = row["seconds"].startswith(">")
            sec = float(TIME_LIMIT) if over else float(row["seconds"])
            series.setdefault(row["impl"], []).append((int(row["n"]), sec, over))

    fig, ax = plt.subplots(figsize=(8, 5))
    for impl, pts in series.items():
        pts.sort()
        ax.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=impl)
        for n, sec, over in pts:
            if over:
                ax.plot([n], [sec], marker="x", color="black", markersize=10)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (число элементов)")
    ax.set_ylabel("время, с (лог. шкала)")
    ax.set_title(f"ЛР7: время сортировки от n (x = больше {TIME_LIMIT} с)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    print(f"график: {png_path}")
    return True


def main() -> None:
    """Прогнать все замеры, вывести таблицу, сохранить CSV и график."""
    random.seed(SEED)
    make_samples()
    rows: list[tuple] = []
    for n in SORT_SIZES:
        rows += bench_sorts(n)
    rows += bench_search()
    rows += bench_two_sum()
    rows += bench_counting()
    print_table(rows)
    save_csv(rows)
    print(f"\nCSV: {OUT_CSV}")
    plot_sorts()


if __name__ == "__main__":
    main()