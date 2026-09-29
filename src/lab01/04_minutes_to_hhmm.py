min = int(input('Минуты: '))
h = min // 60
m = min % 60

print(f'{h}:{m:02d}')