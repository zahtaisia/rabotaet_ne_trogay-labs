f = open('lab_01/src/06ex.txt')

N = int(f.readline())
och = 0
zaoch = 0
for i in range(N):
    fa, im, v, form = f.readline().split()
    v = float(v)
    if form == 'True':
        och += 1
    else:
        zaoch += 1
        
print(f'Очная форма: {och}, заочная форма: {zaoch}')

    