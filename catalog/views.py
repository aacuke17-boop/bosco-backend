from django.shortcuts import render

# Create your views here.
import random
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
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
    return HttpResponse(f'Додано {count} нових записів')
