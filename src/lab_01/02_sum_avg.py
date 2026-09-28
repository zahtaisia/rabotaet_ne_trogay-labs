a = float(input('a: ').replace(',', '.'))
b = float(input('b: ').replace(',', '.'))
sum = a + b
avg = round(sum / 2, 2)
print(f'{sum=}; {avg=}')