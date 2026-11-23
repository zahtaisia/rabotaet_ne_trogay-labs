from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def _check_str(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}: ожидается непустая строка, получено {value!r}")


def _check_birthdate(value):
    if not isinstance(value, str):
        raise ValueError(f"birthdate: ожидается строка YYYY-MM-DD, получено {value!r}")
    # fromisoformat в Python 3.11+ принимает и "20070514", поэтому формат проверяем явно
    if len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError(f"birthdate: {value!r} не соответствует формату YYYY-MM-DD")
    try:
        d = date.fromisoformat(value)
    except ValueError as e:
        raise ValueError(f"birthdate: {value!r} — такой даты не существует ({e})") from None
    if d > date.today():
        raise ValueError(f"birthdate: {value!r} находится в будущем")


def _check_gpa(value):
    # bool — подкласс int, поэтому отсекаем его отдельно
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"gpa: ожидается число, получено {value!r}")
    if not (0 <= value <= 5):
        raise ValueError(f"gpa: {value} вне диапазона 0..5")

def validate_student(rec):
    if not isinstance(rec, dict):
        raise ValueError(f"запись должна быть словарём, получено {type(rec).__name__}")
    keys = set(rec)
    expected = set(STUDENT_FIELDS)
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        raise ValueError(f"неверный набор ключей: нет {missing}, лишние {extra}")
    _check_str("fio", rec["fio"])
    _check_birthdate(rec["birthdate"])
    _check_str("group", rec["group"])
    _check_gpa(rec["gpa"])


def make_student(fio, birthdate, group, gpa):
    rec = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
    validate_student(rec)          # вся логика проверок в одном месте
    rec["gpa"] = float(gpa)        # int допустим, но храним float
    return rec


def student_age(rec, today=None):
    b = date.fromisoformat(rec["birthdate"])
    today = today or date.today()
    # вычитаем 1, если день рождения в этом году ещё не наступил
    return today.year - b.year - ((today.month, today.day) < (b.month, b.day))


def _years_word(n):
    if 11 <= n % 100 <= 14:
        return "лет"
    last = n % 10
    if last == 1:
        return "год"
    if 2 <= last <= 4:
        return "года"
    return "лет"


def format_student(rec):
    parts = rec["fio"].split()
    initials = "".join(p[0] + "." for p in parts[1:])
    short = f"{parts[0]} {initials}".strip()
    age = student_age(rec)
    return f"{short} ({rec['group']}), {age} {_years_word(age)}, GPA {rec['gpa']:.2f}"


def student_to_dict(rec):
    validate_student(rec)
    return {k: rec[k] for k in STUDENT_FIELDS}   # новый словарь, не тот же объект


def student_from_dict(d):
    if not isinstance(d, dict):
        raise ValueError(f"ожидался словарь, получено {type(d).__name__}")
    missing = [k for k in STUDENT_FIELDS if k not in d]
    if missing:
        raise ValueError(f"в записи нет ключей: {missing}")
    # берём ровно нужные ключи; gpa приводится к float внутри make_student
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])

if __name__ == "__main__":
    
    print(make_student("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 4))

    for args in [
        ("Иванов Иван", "2003-02-30", "БИВТ-26-6-1", 4.3),
        ("Иванов Иван", "2007-05-14", "БИВТ-26-6-1", 7),
    ]:
        try:
            make_student(*args)
        except ValueError as e:
            print("ValueError:", e)

    s = make_student("Иванов Иван Иванович", "2007-09-20", "БИВТ-26-6-1", 4.3)
    print(student_age(s, date(2026, 9, 19)))   # 18
    print(student_age(s, date(2026, 9, 20)))   # 19
    print(format_student(s))
    c = student_to_dict(s)
    print(c == s, c is s)                      # True False
    print(student_from_dict({"fio": "Петров Пётр", "birthdate": "2005-01-01", "group": "Б-1", "gpa": 5}))