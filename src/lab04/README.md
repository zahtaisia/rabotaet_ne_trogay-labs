# Лабораторная работа 4

## Задание A

Результат работы:
1. Выполняется кодировка по умолчанию UTF-8, другую передают параметром encoding, например cp1251.
2. Ошибки FileNotFoundError и UnicodeDecodeError не перехватываются.
3. Файл читается целиком. В реальных задачах большие файлы стоит читать построчно.
4. Описание краевых случаев (пустой файл, пустой rows, только заголовок).

Ручной мини-тест `io_txt_csv.py` для README:
Запуск из корня репозитория:
```
python3 -m src.lab04.test_A
```
```python 
from src.io_txt_csv import read_text, write_csv
txt = read_text("data/input.txt")  # должен вернуть строку
write_csv([("word","count"),("test",3)], "data/check.csv")  # создаст CSV
```
Скрипт читает `data/lab04/input.txt` и создаёт `data/lab04/check.csv`.

![Запуск мини-теста](../../images/lab04/img01.png)
Рис.1 Запуск мини-теста

### Задание A: крайние случаи

**1. Пустой входной файл -> возвращается пустая строка**
```
python3 -c "from src.lab04.io_txt_csv import read_text; print(repr(read_text('data/lab04/empty.txt')))"
```
Ожидаемый результат: `''`
![](../../images/lab04/img02.png)
Рис. 2 read_text для пустого файла возвращает пустую строку

**2. `write_csv` с пустым `rows` и `header=None` → пустой файл**
```
python3 -c "from src.lab04.io_txt_csv import write_csv; write_csv([], 'data/lab04/empty.csv')"
ls -l data/lab04/empty.csv
```
![](../../images/lab04/img03.png)
Рис.3 Пустой rows без заголовка: файл создан, размер 0 байт

**3. `write_csv` с пустым `rows` и `header=("a","b")` → только заголовок**
```
python3 -c "from src.lab04.io_txt_csv import write_csv; write_csv([], 'data/lab04/header_only.csv', header=('a','b'))"
cat data/lab04/header_only.csv
```
Ожидаемый результат: `a,b`
![](../../images/lab04/img04.png)
Рис.4 Пустой rows с заголовком: в файле только строка a,b

**4. Строки разной длины → `ValueError`**
```
python3 -c "from src.lab04.io_txt_csv import write_csv; write_csv([(1,2),(3,)], 'data/lab04/bad.csv')"
```
Ожидаемый результат: ошибка `ValueError: Все строки (и заголовок) должны быть одинаковой длины`.
![](../../images/lab04/img05.png)
Рис.5 Строки разной длины вызывают ValueError

**5. Очень большой файл**

Файл читается целиком, это допустимо по ТЗ. В реальных задачах большие файлы
стоит читать построчно, чтобы не загружать весь файл в память.