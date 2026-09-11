a = float(input('Введите первое число: ').replace(',', '.'))
b = float(input('Введите втрое число:'))
sum = a + b
avg = round(sum / 2, 2)
print(f'{sum=}, {avg=}')