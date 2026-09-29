n = int(input('in_1:'))
och = 0
zaoch = 0
for i in range(n):
    vv_date = str(input(f'in_{i+2}:'))
    fa, im, v, form = vv_date.split()
    v = float(v)
    if form == 'True':
        och += 1
    else:
        zaoch += 1
        
print(f'Очная форма: {och}, заочная форма: {zaoch}')

    