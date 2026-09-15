price = int(input('Введите цену товара: '))
discount = int(input('Введите скидку:'))
vat = int(input('Введите НДС:'))

base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount

print(f'База после скидки: {base:.2f} ₽')
print(f'НДС:{vat_amount:>21.2f} ₽')
print(f'Итого к оплате:{total:>11.2f} ₽')