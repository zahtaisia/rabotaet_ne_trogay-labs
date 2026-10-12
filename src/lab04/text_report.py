"""ЛР4, задание B (+★): отчёт по частотам слов для одного или нескольких файлов.

Запуск из корня репозитория:
    python3 src/lab04/text_report.py
    python3 src/lab04/text_report.py --in data/lab04/input.txt --encoding cp1251
    python3 src/lab04/text_report.py --in data/lab04/a.txt data/lab04/b.txt \
        --per-file data/lab04/report_per_file.csv --total data/lab04/report_total.csv
    python3 src/lab04/text_report.py --table
"""

import argparse #читает параметры из командной строки
import sys #даёт доступ к системным вещам: список путей поиска модулей и exit
from collections import Counter
from pathlib import Path

# добавляем корень репозитория в пути поиска модулей
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.lab04.io_txt_csv import read_text, write_csv  # noqa: E402 #просит редактор не ругаться, что импорты не в самом верху
from src.lib.text import normalize, tokenize, count_freq  # noqa: E402  (из ЛР3)


def frequencies_from_text(text: str) -> dict[str, int]:
    """Считает частоты слов в тексте (нормализация и токенизация из ЛР3).

    Args:
        text: исходный текст.

    Returns:
        Словарь {слово: количество}. Для пустого текста он пустой.
    """
    return count_freq(tokenize(normalize(text)))


def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    """Сортирует частоты: count по убыванию, при равенстве слово по возрастанию.

    Args:
        freq: словарь {слово: количество}.

    Returns:
        Список пар (слово, количество).
    """
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))


def format_table(rows: list[tuple[str, int]], header: tuple[str, str] = ("word", "count")) -> str:
    """Формирует текстовую таблицу, ширина столбцов подбирается по максимуму.

    Args:
        rows: строки таблицы (слово, количество).
        header: заголовки двух столбцов.

    Returns:
        Таблица одной строкой с переносами.
    """
    w0 = max([len(header[0])] + [len(word) for word, _ in rows])
    w1 = max([len(header[1])] + [len(str(count)) for _, count in rows])
    lines = [f"{header[0]:<{w0}} | {header[1]:>{w1}}", f"{'-' * w0}-+-{'-' * w1}"]
    lines += [f"{word:<{w0}} | {count:>{w1}}" for word, count in rows]
    return "\n".join(lines)


def main() -> None:
    """Точка входа: разбирает аргументы, строит отчёты и печатает резюме.

    Аргументы командной строки:
        --in: один или несколько входных файлов (по умолчанию data/lab04/input.txt).
        --out: CSV word,count по всем файлам вместе (по умолчанию data/lab04/report.csv).
        --encoding: кодировка входных файлов (по умолчанию utf-8), например cp1251.
        --per-file: (★) CSV file,word,count по каждому файлу отдельно.
        --total: (★) ещё один сводный CSV word,count.
        --table: (★) дополнительно вывести таблицу в консоль.

    Краевые случаи:
        - файл не найден: сообщение об ошибке и выход с кодом 1;
        - пустой вход: в CSV только заголовок.
    """
    parser = argparse.ArgumentParser(description="Отчёт по частотам слов")#создает парсер
    parser.add_argument("--in", dest="inputs", nargs="+", default=["data/lab04/input.txt"],
                        help="входные файлы (по умолчанию data/lab04/input.txt)")#описывает правила для парсера
    parser.add_argument("--out", default="data/lab04/report.csv",
                        help="выходной CSV (по умолчанию data/lab04/report.csv)")
    parser.add_argument("--encoding", default="utf-8",
                        help="кодировка входных файлов (по умолчанию utf-8)")
    parser.add_argument("--per-file", default=None, help="CSV file,word,count (★)")
    parser.add_argument("--total", default=None, help="сводный CSV word,count (★)")
    parser.add_argument("--table", action="store_true", help="вывести таблицу в консоль (★)")
    args = parser.parse_args()#разбирает аргументы командной строки и возвращает объект с полями, соответствующими аргументам

    per_file: dict[str, dict[str, int]] = {}
    total: Counter = Counter()
    for path in args.inputs:
        try:
            text = read_text(path, encoding=args.encoding)
        except FileNotFoundError:
            print(f"Ошибка: файл не найден: {path}")
            sys.exit(1)
        freq = frequencies_from_text(text)
        per_file[Path(path).name] = freq
        total.update(freq)

    rows = sorted_word_counts(total)

    write_csv(rows, args.out, header=("word", "count"))
    if args.total:
        write_csv(rows, args.total, header=("word", "count"))
    if args.per_file:
        per_file_rows = [
            (name, word, count)
            for name in sorted(per_file) # внешний цикл: по файлам
            for word, count in sorted_word_counts(per_file[name]) # внутренний цикл: по словам файла
        ]
        write_csv(per_file_rows, args.per_file, header=("file", "word", "count"))

    print(f"Всего слов: {sum(total.values())}")
    print(f"Уникальных слов: {len(total)}")
    print("Топ-5:")
    for word, count in rows[:5]:
        print(f"{word}:{count}")

    if args.table:
        print()
        print(format_table(rows))


if __name__ == "__main__":
    main()