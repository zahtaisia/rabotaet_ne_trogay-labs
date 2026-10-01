import re
import unicodedata

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    text = text.casefold() if casefold else text.lower()

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
        
    text = "".join(
        " " if unicodedata.category(ch) == "Cc" else ch for ch in text
    )

    return " ".join(text.split())


def tokenize(text: str) -> list[str]:
    return re.compile(r"\w+(?:-\w+)*").findall(text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return dict(sorted(freq.items()))


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    if n <= 0:
        return []
    return sorted(freq.items(), key=lambda p: (-p[1], p[0]))[:n]

