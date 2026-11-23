import json
from pathlib import Path

from src.lab08.models import make_student, student_to_dict, student_from_dict


def students_to_json(students, path):
    # student_to_dict заодно валидирует каждую запись перед записью в файл
    data = [student_to_dict(s) for s in students]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def students_from_json(path, strict=True):
    """Читает JSON-массив записей.

    strict=True  (по умолчанию): первая же битая запись -> ValueError с номером и причиной.
    strict=False: битые записи пропускаются, в конце печатается сводка.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать массив записей")

    result = []
    skipped = []
    for number, item in enumerate(data, start=1):   # нумерация с 1
        try:
            result.append(student_from_dict(item))
        except ValueError as e:
            if strict:
                raise ValueError(f"запись №{number}: {e}") from None
            skipped.append((number, str(e)))

    if skipped:
        print(f"Пропущено записей: {len(skipped)}")
        for number, reason in skipped:
            print(f"  №{number}: {reason}")
    return result


if __name__ == "__main__":
    # 1. корректные записи туда-обратно
    students = students_from_json("data/lab08/students_input.json")
    print(f"Прочитано: {len(students)}")
    students_to_json(students, "data/lab08/students_output.json")
    print("Записано в students_output.json")
    print("Совпадает при чтении обратно:",
          students_from_json("data/lab08/students_output.json") == students)

    # 2. битые записи: политика strict
    print("\n--- strict ---")
    try:
        students_from_json("data/lab08/students_bad.json")
    except ValueError as e:
        print("ValueError:", e)

    # 3. битые записи: политика skip
    print("\n--- skip ---")
    ok = students_from_json("data/lab08/students_bad.json", strict=False)
    print("Загружено валидных:", len(ok))