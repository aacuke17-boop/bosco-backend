import random
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Product

NAMES = [
    ('М’яч футбольний', 'Футбол', 'Шкіра'),
    ('Ракетка тенісна', 'Теніс', 'Графіт'),
    ('Гантелі 5 кг', 'Фітнес', 'Метал'),
    ('Скакалка', 'Фітнес', 'Пластик'),
    ('Боксерські рукавиці', 'Бокс', 'Шкірозамінник'),
    ('Велошолом', 'Велоспорт', 'Пластик'),
    ('Йога-килимок', 'Йога', 'ТПЕ'),
    ('Баскетбольний м’яч', 'Баскетбол', 'Гума'),
    ('Лижні палиці', 'Зимові види', 'Алюміній'),
    ('Окуляри для плавання', 'Плавання', 'Силікон'),
]
BRANDS = ['Nike', 'Adidas', 'Puma', 'Wilson', 'Decathlon', 'Reebok']


def products(request):
    return render(request, 'catalog/products.html', {
        'products': Product.objects.all(),
    })


def replenish(request, count):
    new_products = []
    for _ in range(count):
        name, category, material = random.choice(NAMES)
        new_products.append(Product(
            name=name,
            category=category,
            material=material,
            brand=random.choice(BRANDS),
            price=Decimal(random.randint(100, 5000)),
        ))
    Product.objects.bulk_create(new_products)
    messages.success(request, f'Додано {count} нових записів')
    return redirect('products')


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        material = request.POST.get('material', '').strip()
        brand = request.POST.get('brand', '').strip()
        price_raw = request.POST.get('price', '').strip().replace(',', '.')

        try:
            price = Decimal(price_raw)
            if price < 0:
                raise InvalidOperation
        except InvalidOperation:
            price = None

        if not all([name, category, material, brand]) or price is None:
            messages.error(request, 'Заповніть усі поля коректно')
            return render(request, 'catalog/add_product.html', {
                'values': request.POST,
            })

        Product.objects.create(
            name=name, category=category, material=material,
            brand=brand, price=price,
        )
        messages.success(request, f'Товар «{name}» додано')
        return redirect('products')

    return render(request, 'catalog/add_product.html')