import re
import unicodedata

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


def tokenize(text: str) -> list[str]:
    """Разбивает текст на слова: \\w+ с возможными дефисами внутри слова.
    Числа считаются словами.
    
     Args:
        text: Строка, обычно уже прошедшая ``normalize``.

    Returns:
        Список слов в порядке их появления в тексте.
    """
    return re.compile(r"\w+(?:-\w+)*").findall(text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Возвращает словарь «слово -> количество».
    
    Args:
        tokens: Список слов (например, результат ``tokenize``).

    Returns:
        Словарь «слово -> количество вхождений»
    """
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return dict(sorted(freq.items()))


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Топ-N по убыванию частоты; при равенстве частот — по алфавиту.
    
    Args:
        freq: Словарь «слово -> количество» (результат ``count_freq``).
        n: Сколько слов вернуть. Если ``n <= 0``, возвращается пустой список.

    Returns:
        Список пар ``(слово, частота)`` длиной не более ``n``.
    """
    if n <= 0:
        return []
    return sorted(freq.items(), key=lambda p: (-p[1], p[0]))[:n]


print('Тест кейсы:')
print(f'''
normalize

{normalize("ПрИвЕт\nМИр\t")}
{normalize("ёжик, Ёлка", yo2e=True)}
{normalize("Hello\r\nWorld")}
{normalize("  двойные   пробелы  ")}
''')

print(f'''
tokenize

{tokenize("привет мир")}
{tokenize("hello,world!!!")}
{tokenize("по-настоящему круто")}
{tokenize("2025 год")}
{tokenize("emoji 😀 не слово")}
''')

print(f'''
count_freq + top_n

{count_freq(["a", "b", "a", "c", "b", "a"])}
{top_n(count_freq(["a", "b", "a", "c", "b", "a"]), n=2)}
{count_freq(["bb","aa","bb","aa","cc"])}
{top_n(count_freq(["bb","aa","bb","aa","cc"]), n=2)}
''')

