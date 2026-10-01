# Лабораторная работа 3
## Задание 1

### 1. Функция `normalize`

```python
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """Нормализует строку.

    casefold=True  -> text.casefold(), иначе text.lower().
    yo2e=True      -> ё/Ё заменяются на е/Е.
    Управляющие символы (\\t, \\r, \\n и др.) заменяются пробелами,
    повторяющиеся пробелы схлопываются, края обрезаются.
    Args:
        text: Исходная строка.
        casefold: Если True, используется ``str.casefold()`` (корректнее для
            Юникода, например «ß» -> «ss»). Если False, используется
            ``str.lower()``.
        yo2e: Если True, все «ё»/«Ё» заменяются на «е»/«Е».

    Returns:
        Нормализованная строка.
    """
    text = text.casefold() if casefold else text.lower()

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
        
    text = "".join(
        " " if unicodedata.category(ch) == "Cc" else ch for ch in text
    )

    return " ".join(text.split())

```
![](../../images/lab03/img01.png)
#### Рис.1 Результат работы функции normalize. Реализовано преобразование строки: риведение к нижнему регистру, замена ё/Ё на е/Е, удаление управляющих символов и лишних пробелов.