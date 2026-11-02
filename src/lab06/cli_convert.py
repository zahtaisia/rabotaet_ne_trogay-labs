"""CLI-конвертеры данных: json2csv, csv2json, csv2xlsx."""

import argparse
import sys

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def build_parser() -> argparse.ArgumentParser:
    """Создаёт парсер с подкомандами json2csv, csv2json, csv2xlsx.

    Returns:
        Настроенный ArgumentParser.
    """
    parser = argparse.ArgumentParser(description="Конвертеры данных (ЛР6)")
    sub = parser.add_subparsers(dest="cmd")

    for name, help_text in (
        ("json2csv", "Конвертировать JSON в CSV"),
        ("csv2json", "Конвертировать CSV в JSON"),
        ("csv2xlsx", "Конвертировать CSV в XLSX"),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--in", dest="input", required=True, help="Входной файл")
        p.add_argument("--out", dest="output", required=True, help="Выходной файл")

    return parser


def main() -> None:
    """Точка входа: вызывает конвертер в зависимости от подкоманды."""
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd is None:
        parser.error("нужно указать подкоманду: json2csv, csv2json или csv2xlsx")

    converters = {
        "json2csv": json_to_csv,
        "csv2json": csv_to_json,
        "csv2xlsx": csv_to_xlsx,
    }

    try:
        converters[args.cmd](args.input, args.output)
        print(f"Готово: {args.input} -> {args.output}")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Ошибка: файл {args.input} не в кодировке UTF-8", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка данных: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()