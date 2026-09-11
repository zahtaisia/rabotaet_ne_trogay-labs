fio = input('Введите ФИО: ')
dl = len(fio.replace(' ', '')) + 2
inic = fio[0]
for i in range(len(fio)-1):
    if fio[i] == ' ':
        if fio[i+1]!= ' ':
            inic+= fio[i+1]
            
print(f"ФИО: {fio}")
print(f'Инициалы: {inic.upper()}.')
print(f'Длина: {dl}')