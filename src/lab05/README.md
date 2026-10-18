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
- JSON<->CSV: порядок колонок — ключи первого объекта, затем новые ключи из остальных объектов в порядке появления; отсутствующие поля и `null` -> пустая строка; вложенные `dict`/`list` записываются как JSON-строка.
- CSV<->JSON: первая строка — обязательный заголовок; все значения сохраняются **строками** (`"age": "22"`); разделитель (`,` `;` табуляция) определяется автоматически.
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

Просмотр результата CSV->JSON (список объектов):

```bash
cat data/lab05/out/people_from_csv.json
```
#сделала фотки до этого момента 
#впереди тест кейсы над ошибками
Проверка количества записей JSON->CSV (исходный JSON и полученный CSV):

```bash
python3 -c "import csv, json; print('Записей в JSON:', len(json.load(open('data/lab05/samples/people.json', encoding='utf-8')))); print('Строк в CSV:', len(list(csv.DictReader(open('data/lab05/out/people_from_json.csv', encoding='utf-8')))))"
```

Проверка количества записей CSV->JSON (исходный CSV и полученный JSON):

```bash
python3 -c "import csv, json; print('Строк в CSV:', len(list(csv.DictReader(open('data/lab05/samples/people.csv', encoding='utf-8'))))); print('Объектов в JSON:', len(json.load(open('data/lab05/out/people_from_csv.json', encoding='utf-8'))))"
```

Ожидаемый вывод проверок:

```
Записей в JSON: 4
Строк в CSV: 4
Строк в CSV: 4
Объектов в JSON: 4
```

![Запуск задания A](images/lab05/A_run.png)

*Скриншот: запуск конвертаций JSON↔CSV, содержимое файлов результата и проверка количества записей.*