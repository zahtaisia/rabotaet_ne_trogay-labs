def format_record(rec: tuple[str, str, float]) -> str:
    """Форматирует запись о студенте в строку.

    Args:
        rec: кортеж (fio, group, gpa): ФИО из 2-3 слов, группа, средний балл.

    Returns:
        Строка вида "Иванов И.И., гр. BIVT-25, GPA 4.60".

    Raises:
        TypeError: если rec не кортеж из 3 элементов или типы полей неверны.
        ValueError: если ФИО не из 2-3 слов или группа пустая.
    """
    if not isinstance(rec, tuple) or len(rec) != 3:
        raise TypeError("запись должна быть кортежем (fio, group, gpa)")

    fio, group, gpa = rec

    if not isinstance(fio, str):
        raise TypeError("fio должно быть строкой")
    if not isinstance(group, str):
        raise TypeError("group должна быть строкой")
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise TypeError("gpa должен быть числом (int или float)")

    parts = fio.split()
    if not parts:
        raise ValueError("пустое ФИО")
    if len(parts) not in (2, 3):
        raise ValueError("ФИО должно состоять из 2 или 3 слов")
    if any(not part.isalpha() for part in parts):
        raise ValueError("ФИО должно состоять только из букв")

    group = " ".join(group.split())
    if not group:
        raise ValueError("пустая группа")

    surname = parts[0].title()
    initials = "".join(name[0].upper() + "." for name in parts[1:])

    return f"{surname} {initials}, гр. {group}, GPA {gpa:.2f}"

print('Тест кейсы:')
print(f'''
format_record
{format_record(("Иванов Иван Иванович", "BIVT-25", 4.6))}
{format_record(("Петров Пётр", "IKBO-12", 5.0))}
{format_record(("Петров Пётр Петрович", "IKBO-12", 5.0))}
{format_record((" сидорова анна сергеевна ", "ABB-01", 3.999))}
''')
#--------------------ValueError
#print(format_record(("  ", "ABB-01", 3.999)))
#print(format_record((" Анна ", "ABB-01", 3.999)))
#print(format_record((" сидорова анна сергеевна ", "", 3.999)))
#print(format_record((" Иванов Ив42 Ив67ович ", "ABB-01", 3.999)))

#--------------------TypeError
print(format_record(("Магомед Магомедов ", "ABB-01", "3.999")))
#print(format_record((["Ойякиви Сергей Александрович"], "BIVT-26-6-1", 3.999)))
#print(format_record(("Люблюмаму Оченьсильно", ["BIVT-26-6-1"], 3.999)))
