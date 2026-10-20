# Лабораторная работа 5

**Цель:** разобраться с форматом JSON, сериализацией и десериализацией, научиться конвертировать табличные данные между JSON, CSV и XLSX.
Все команды запускаются **из корня репозитория** (пути в коде относительные).

## Подготовка
Установка единственной внешней зависимости (`openpyxl`, нужна только для XLSX):

```bash
python3 -m pip install -r requirements.txt
```

---

## Задание A — JSON <-> CSV

### Задание

Модуль `src/lab05/json_csv.py` с двумя функциями:

- `json_to_csv(json_path, csv_path)` — JSON (список словарей) -> CSV;
- `csv_to_json(csv_path, json_path)` — CSV -> JSON (список словарей).

**Допущения:**
- JSON -> CSV: порядок колонок — ключи первого объекта, затем новые ключи из остальных объектов в порядке появления; отсутствующие поля и `null` -> пустая строка; вложенные `dict`/`list` записываются как JSON-строка.
- CSV -> JSON: первая строка — обязательный заголовок; все значения сохраняются **строками** (`"age": "22"`); разделитель (`,` `;` табуляция) определяется автоматически.
- Кодировка строго UTF-8, запись JSON через `ensure_ascii=False, indent=2`.

### Запуск

Конвертация JSON->CSV и CSV->JSON:

```bash
python3 -c "from src.lab05.json_csv import json_to_csv, csv_to_json; json_to_csv('data/lab05/samples/people.json', 'data/lab05/out/people_from_json.csv'); csv_to_json('data/lab05/samples/people.csv', 'data/lab05/out/people_from_csv.json')"
```

Просмотр результата JSON->CSV (заголовок и строки):

```bash
cat data/lab05/out/people_from_json.csv
```
![](../../images/lab05/img01.png)
Рис.1 просмотр содержимого файла people_from_json.csv

Просмотр результата CSV->JSON (список объектов):

```bash
cat data/lab05/out/people_from_csv.json
```
![](../../images/lab05/img02.png)
Рис.2 просмотр содержимого файла people_from_csv.json

Проверка количества записей JSON->CSV (исходный JSON и полученный CSV):

```bash
python3 -c "import csv, json; print('Записей в JSON:', len(json.load(open('data/lab05/samples/people.json', encoding='utf-8')))); print('Строк в CSV:', len(list(csv.DictReader(open('data/lab05/out/people_from_json.csv', encoding='utf-8')))))"
```
![](../../images/lab05/img03.png)
Рис.3 Вывод проверки количества записей

Проверка количества записей CSV->JSON (исходный CSV и полученный JSON):

```bash
python3 -c "import csv, json; print('Строк в CSV:', len(list(csv.DictReader(open('data/lab05/samples/people.csv', encoding='utf-8'))))); print('Объектов в JSON:', len(json.load(open('data/lab05/out/people_from_csv.json', encoding='utf-8'))))"
```
![](../../images/lab05/img04.png)
Рис.4 Вывод проверки количества записей

### ДО -> ПОСЛЕ
![](../../images/lab05/img05.png)  ![](../../images/lab05/img06.png)
Рис.5 и Рис.6 Результат работы программы по преобразованию файла из CSV в JSON

![](../../images/lab05/img07.png) ![](../../images/lab05/img08.png)
Рис.7 и Рис.8 Результат работы программы по преобразованию файла из JSON в CSV

### Тест-кейсы

Запуск тестов задания A:

```bash
python3 -m unittest src.lab05.test_lab05.TestJsonToCsv src.lab05.test_lab05.TestCsvToJson -v
```

| Функция | Тест-кейс | Ожидаемый результат |
|---|---|---|
| `json_to_csv` | Обычный JSON со списком словарей (с кириллицей) | CSV с верным заголовком и строками |
| `json_to_csv` | У части объектов нет некоторых полей | Колонки объединяются, пропуски — пустые строки |
| `csv_to_json` | Обычный CSV | Список словарей, все значения — строки |
| `csv_to_json` | CSV с разделителем `;` | Читается так же, как с запятой |
| `csv_to_json` | Кириллица в данных | В JSON буквы, а не `\uXXXX` |
| оба | CSV → JSON → CSV | Количество записей до и после совпадает |

![Тесты задания A](images/lab05/A_tests.png)

*Скриншот: результат тестов задания A (все тесты `ok`).*

### Ошибки

| Ситуация | Исключение | Сообщение |
|---|---|---|
| Входной файл не существует | `FileNotFoundError` | `Файл не найден: ...` |
| Неверное расширение файла | `ValueError` | `Неверный тип файла: ожидался .json, получен '.csv'` |
| Пустой список `[]` в JSON | `ValueError` | `Пустой JSON или неподдерживаемая структура` |
| В JSON не список (например, объект) | `ValueError` | `Пустой JSON или неподдерживаемая структура` |
| Список содержит не словари | `ValueError` | `JSON должен быть списком словарей` |
| Синтаксическая ошибка в JSON | `ValueError` | `Некорректный JSON: ...` |
| Пустой CSV | `ValueError` | `Пустой CSV` |
| CSV только с заголовком, без данных | `ValueError` | `CSV содержит только заголовок, данных нет` |
| Пустые или повторяющиеся названия колонок | `ValueError` | `CSV без заголовка или с пустыми названиями колонок` / `В заголовке CSV есть повторяющиеся колонки` |

Показать ошибку «файл не найден»:

```bash
python3 -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/lab05/samples/nope.json', 'data/lab05/out/x.csv')"
```

Показать ошибку «неверный тип файла» (подаём CSV вместо JSON):

```bash
python3 -c "from src.lab05.json_csv import json_to_csv; json_to_csv('data/lab05/samples/people.csv', 'data/lab05/out/x.csv')"
```

![Ошибки задания A](images/lab05/A_errors.png)

*Скриншот: `FileNotFoundError` и `ValueError` при неверных входных данных.*