"""CLI-утилиты для работы с текстом: cat и stats."""

import argparse
import sys
from pathlib import Path

from src.lib.text import normalize, tokenize, count_freq, top_n


def read_text(path: str) -> str:
    """Читает текстовый файл целиком.

    Args:
        path: Путь к файлу.

    Returns:
        Содержимое файла в виде строки.

    Raises:
        FileNotFoundError: Если файл не существует.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")
    return p.read_text(encoding="utf-8")


def cmd_cat(input_path: str, numbered: bool) -> None:
    """Выводит файл построчно, при необходимости с нумерацией.

    Args:
        input_path: Путь к входному файлу.
        numbered: Если True, перед строками выводятся номера.
    """
    text = read_text(input_path)
    for i, line in enumerate(text.splitlines(), start=1):
        print(f"{i:>4}  {line}" if numbered else line)


def cmd_stats(input_path: str, top: int) -> None:
    """Выводит топ-N самых частых слов текста.

    Args:
        input_path: Путь к входному файлу.
        top: Сколько слов показать.
    """
    text = read_text(input_path)
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{top}:")
    for word, count in top_n(freq, top):
        print(f"{word}:{count}")


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов с подкомандами cat и stats.

    Returns:
        Настроенный ArgumentParser.
    """
    parser = argparse.ArgumentParser(description="CLI-утилиты лабораторной №6 (текст)")
    sub = parser.add_subparsers(dest="command")

    p_cat = sub.add_parser("cat", help="Вывести содержимое файла")
    p_cat.add_argument("--input", required=True, help="Путь к входному файлу")
    p_cat.add_argument("-n", action="store_true", help="Нумеровать строки")

    p_stats = sub.add_parser("stats", help="Частоты слов в тексте")
    p_stats.add_argument("--input", required=True, help="Путь к текстовому файлу")
    p_stats.add_argument(
        "--top", type=int, default=5, help="Сколько слов выводить (по умолчанию 5)"
    )

    return parser


def main() -> None:
    """Точка входа: разбирает аргументы и вызывает нужную подкоманду."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.error("нужно указать подкоманду: cat или stats")

    try:
        if args.command == "cat":
            cmd_cat(args.input, args.n)
        elif args.command == "stats":
            if args.top <= 0:
                parser.error("--top должен быть положительным числом")
            cmd_stats(args.input, args.top)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()