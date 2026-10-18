"""Конвертация JSON <-> CSV (ЛР5, задание A).

Функции ничего не печатают в stdout, только читают и пишут файлы.
Кодировка — UTF-8, пути — относительные (от корня репозитория).
"""
import csv
import json
from pathlib import Path


def _check_input(path: str, suffix: str) -> Path:
    """Проверяет расширение и существование входного файла.

    Args:
        path (str): Путь к входному файлу.
        suffix (str): Ожидаемое расширение, например ".json".

    Returns:
        Path: Путь к файлу в виде объекта Path.

    Raises:
        ValueError: Если расширение файла не совпадает с ожидаемым.
        FileNotFoundError: Если файл не существует.
    """
    p = Path(path)
    if p.suffix.lower() != suffix:
        raise ValueError(f"Неверный тип файла: ожидался {suffix}, получен '{p.suffix}'")
    if not p.is_file():
        raise FileNotFoundError(f"Файл не найден: {p}")
    return p


def _check_output(path: str, suffix: str) -> Path:
    """Проверяет расширение выходного файла и создаёт папку, если её нет.

    Args:
        path (str): Путь к выходному файлу.
        suffix (str): Ожидаемое расширение, например ".csv".

    Returns:
        Path: Путь к файлу в виде объекта Path.

    Raises:
        ValueError: Если расширение файла не совпадает с ожидаемым.
    """
    p = Path(path)
    if p.suffix.lower() != suffix:
        raise ValueError(f"Неверный тип файла: ожидался {suffix}, получен '{p.suffix}'")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _to_cell(value) -> str:
    """Преобразует значение из JSON в строку для ячейки CSV.

    Args:
        value: Значение из JSON (строка, число, None, dict, list и т.д.).

    Returns:
        str: Пустая строка для None, JSON-строка для dict и list,
            иначе str(value).
    """
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)

def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл (список словарей) в CSV.

    Порядок колонок: ключи первого объекта, затем новые ключи из
    следующих объектов в порядке появления. Отсутствующие поля
    заполняются пустыми строками. Кодировка UTF-8.

    Args:
        json_path (str): Путь к входному .json файлу.
        csv_path (str): Путь к выходному .csv файлу.

    Raises:
        ValueError: Если расширение неверное, JSON некорректный или пустой,
            не является списком либо содержит не только словари.
        FileNotFoundError: Если входной файл не существует.
    """
    src = _check_input(json_path, ".json")
    dst = _check_output(csv_path, ".csv")

    try:
        with src.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON: {e}") from e

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("JSON должен быть списком словарей")

    fieldnames: list[str] = []
    for item in data:
        for key in item:
            if key not in fieldnames:
                fieldnames.append(key)
    if not fieldnames:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    with dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow({k: _to_cell(item.get(k, "")) for k in fieldnames})
            
def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV-файл в JSON (список словарей).

    Первая строка CSV — обязательный заголовок. Все значения
    сохраняются как строки. Запись выполняется через
    json.dump(..., ensure_ascii=False, indent=2). Разделитель
    (запятая, точка с запятой или табуляция) определяется автоматически.

    Args:
        csv_path (str): Путь к входному .csv файлу.
        json_path (str): Путь к выходному .json файлу.

    Raises:
        ValueError: Если расширение неверное, файл пустой, нет заголовка
            (или он содержит пустые/повторяющиеся названия), нет строк
            с данными либо в строке больше значений, чем в заголовке.
        FileNotFoundError: Если входной файл не существует.
    """
    src = _check_input(csv_path, ".csv")
    dst = _check_output(json_path, ".json")

    # utf-8-sig: корректно читает и обычный UTF-8, и UTF-8 с BOM (Excel)
    with src.open(newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        if not sample.strip():
            raise ValueError("Пустой CSV")
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)

        header = reader.fieldnames
        if not header or any(not (h or "").strip() for h in header):
            raise ValueError("CSV без заголовка или с пустыми названиями колонок")
        if len(set(header)) != len(header):
            raise ValueError("В заголовке CSV есть повторяющиеся колонки")

        rows = []
        for row in reader:
            if None in row:  # в строке больше значений, чем в заголовке
                raise ValueError("Строка CSV содержит больше значений, чем заголовок")
            rows.append({k: (v if v is not None else "") for k, v in row.items()})

    if not rows:
        raise ValueError("CSV содержит только заголовок, данных нет")

    with dst.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        
        
