from src.lib.text import normalize, tokenize, count_freq, top_n
import os

TABLE_MODE = os.getenv("TABLE_MODE", "0") == "1"
'''Порядок работы:
        1. Читает одну строку через ``input()``.
        2. Нормализует текст, разбивает на слова и считает частоты.
        3. Печатает обычный вывод: всего слов, уникальных слов, топ-5.
        4. Печатает топ-5 в виде таблицы «слово | частота». Ширина первого
           столбца равна длине самого длинного слова из топа (но не меньше
           длины заголовка «слово»).'''
           


def main() -> None:
    """Читает строку из stdin, считает слова и печатает результат.
    Args:
        Нет. Текст читается из stdin через ``input()``.

    Returns:
        None. Результат печатается в stdout.
        
    Raises:
        ValueError: Если текст не введён (нет ввода, пустая строка или
            только пробелы).
    """
    try:
        text = input()
    except EOFError:
        raise ValueError("Текст не введён") from None

    if not text.strip():
        raise ValueError("Текст не введён")

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, 5)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print("Топ-5:")

    if TABLE_MODE:
        width = max([len("слово")] + [len(word) for word, _ in top])
        print("слово".ljust(width) + " | частота")
        print("-" * (width + 10))
        for word, count in top:
            print(word.ljust(width) + " | " + str(count))
    else:
        for word, count in top:
            print(f"{word}:{count}")


if __name__ == "__main__":
    main()
    
