# Лабораторная работа 6

**Цель:** научиться создавать консольные утилиты с аргументами командной строки, подкомандами и флагами на модуле `argparse`.
Все команды запускаются **из корня репозитория**.

## Структура

- `src/lab06/cli_text.py` — подкоманды `cat`, `stats`
- `src/lab06/cli_convert.py` — подкоманды `json2csv`, `csv2json`, `csv2xlsx`

---

## Задание A — cli_text.py

| Подкоманда | Параметры | Описание |
|---|---|---|
| `cat` | `--input <path>`, `-n` | Вывод файла построчно, `-n` — с нумерацией |
| `stats` | `--input <txt>`, `--top N` (по умолчанию 5) | Всего слов, уникальных слов, топ-N частых слов |

Справка:

```bash
python3 -m src.lab06.cli_text --help
```

![](../../images/lab06/img01.png)
Рис.1 Справка cli_text.py

Вывод файла с нумерацией строк:

```bash
python3 -m src.lab06.cli_text cat --input data/lab05/samples/people.csv -n
```

![](../../images/lab06/img02.png)
Рис.2 Подкоманда cat с флагом -n

Частоты слов:

```bash
python3 -m src.lab06.cli_text stats --input data/lab05/samples/people.txt --top 5
```

![](../../images/lab06/img03.png)
Рис.3 Подкоманда stats

### Проверка ошибок

Файл не найден:

```bash
python3 -m src.lab06.cli_text cat --input nofile.txt
```

![](../../images/lab06/img04.png)
Рис.4 Ошибка: входной файл не существует

Неверный аргумент:

```bash
python3 -m src.lab06.cli_text stats --input data/lab05/samples/people.txt --top abc
```

![](../../images/lab06/img05.png)
Рис.5 Ошибка: --top должен быть числом

### Справка по подкомандам

```bash
python3 -m src.lab06.cli_text cat --help
```

![](../../images/lab06/img11.png)
Рис.6 Справка подкоманды cat

```bash
python3 -m src.lab06.cli_text stats --help
```

![](../../images/lab06/img12.png)
Рис.7 Справка подкоманды stats
---

## Задание B — cli_convert.py

| Подкоманда | Параметры | Описание |
|---|---|---|
| `json2csv` | `--in`, `--out` | JSON -> CSV |
| `csv2json` | `--in`, `--out` | CSV -> JSON |
| `csv2xlsx` | `--in`, `--out` | CSV -> XLSX |

Справка:

```bash
python3 -m src.lab06.cli_convert --help
```

![](../../images/lab06/img06.png)
Рис.8 Справка cli_convert.py

JSON -> CSV:

```bash
python3 -m src.lab06.cli_convert json2csv --in data/lab05/samples/people.json --out data/lab05/out/people.csv
```

![](../../images/lab06/img07.png)
Рис.9 Подкоманда json2csv

CSV -> JSON:

```bash
python3 -m src.lab06.cli_convert csv2json --in data/lab05/samples/people.csv --out data/lab05/out/people.json
```

![](../../images/lab06/img08.png)
Рис.10 Подкоманда csv2json

CSV -> XLSX:

```bash
python3 -m src.lab06.cli_convert csv2xlsx --in data/lab05/samples/people.csv --out data/lab05/out/people.xlsx
```

![](../../images/lab06/img09.png)
Рис.11 Подкоманда csv2xlsx

### Проверка ошибок

Неверный тип файла:

```bash
python3 -m src.lab06.cli_convert json2csv --in data/lab05/samples/people.csv --out data/lab05/out/x.csv
```

![](../../images/lab06/img10.png)
Рис.12 Ошибка: вместо .json передан .csv

Файл не найден:

```bash
python3 -m src.lab06.cli_convert csv2json --in data/lab05/samples/nope.csv --out data/lab05/out/x.json
```

![](../../images/lab06/img13.png)
Рис.13 Ошибка: входной файл не существует

### Справка по подкомандам

```bash
python3 -m src.lab06.cli_convert json2csv --help
```

![](../../images/lab06/img14.png)
Рис.14 Справка подкоманды json2csv

```bash
python3 -m src.lab06.cli_convert csv2json --help
```

![](../../images/lab06/img15.png)
Рис.15 Справка подкоманды csv2json

```bash
python3 -m src.lab06.cli_convert csv2xlsx --help
```

![](../../images/lab06/img16.png)
Рис.16 Справка подкоманды csv2xlsx

### ДО -> ПОСЛЕ

![](../../images/lab06/img17.png) ![](../../images/lab06/img18.png)
Рис.17 и Рис.18 Результат работы csv2json (исходный CSV и полученный JSON)

![](../../images/lab06/img19.png)
Рис.19 Файл people.xlsx, полученный через csv2xlsx