"""Ввод/вывод для ЛР4: чтение текста и запись CSV."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Sequence


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские директории для path, если их нет."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает файл целиком и возвращает содержимое одной строкой.

    Args:
        path: путь к файлу.
        encoding: кодировка файла (по умолчанию UTF-8). Чтобы выбрать другую
            кодировку, передайте её явно, например: encoding="cp1251".

    Raises:
        FileNotFoundError: файл не найден (не перехватывается).
        UnicodeDecodeError: кодировка не подходит (не перехватывается).

    Пустой файл даёт пустую строку.
    """
    return Path(path).read_text(encoding=encoding)


def write_csv(
    rows: Iterable[Sequence],
    path: str | Path,
    header: tuple[str, ...] | None = None,
) -> None:
    """Создаёт или перезаписывает CSV-файл (разделитель запятая, UTF-8).

    Args:
        rows: строки данных (кортежи или списки).
        path: путь к CSV-файлу; родительские папки создаются автоматически.
        header: необязательный заголовок, записывается первой строкой.

    Raises:
        ValueError: если строки (или заголовок) имеют разную длину.

    Пустой rows без header даёт пустой файл; с header в файле только заголовок.
    """
    rows = list(rows)
    lengths = {len(r) for r in rows}
    if header is not None:
        lengths.add(len(header))
    if len(lengths) > 1:
        raise ValueError("Все строки (и заголовок) должны быть одинаковой длины")

    ensure_parent_dir(path)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        w.writerows(rows)