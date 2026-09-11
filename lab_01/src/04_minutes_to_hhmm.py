min = int(input('Ведите количество минут: '))
h = min // 60
m = min % 60
print(f'Минуты: {min:02d}')
print(f'{h}:{m:02d}')