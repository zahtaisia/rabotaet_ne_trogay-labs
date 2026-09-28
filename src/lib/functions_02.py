def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not (len(nums)):
        raise ValueError ('пустая строка')
    else:
        mx = nums[0]
        mn = nums[0]
        for n in nums:
            if n > mx:
                mx = n
            if n < mn:
                mn = n
        return mn, mx
    
    
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    ans = []
    while len(nums) > 0:
        mn = nums[0]
        for n in nums:
            if n < mn and n not in ans:
                mn = n
        ans.append(mn)
        while mn in nums:
            nums.remove(mn)
    return ans


def flatten(mat: list[list | tuple]) -> list:
    if not len(mat):
        raise ValueError ('пустая строка')
    else:
        pr = []
        for row in mat:
            if type(row) != list and type(row) != tuple:
                raise TypeError ('строка не является строкой строк матрицы')
            pr.extend(row)
        return pr
    

def transpose(mat: list[list[float | int]]) -> list[list]:
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [list(col) for col in zip(*mat)]

def row_sums(mat: list[list[float | int]]) -> list[float]:
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [sum(row) for row in mat]

def col_sums(mat: list[list[float | int]]) -> list[float]:
    if mat and any(len(row) != len(mat[0]) for row in mat):
        raise ValueError("рваная матрица")
    return [sum(col) for col in zip(*mat)]

def format_record(rec: tuple[str, str, float]) -> str:
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