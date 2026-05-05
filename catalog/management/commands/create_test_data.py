from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Создаёт тестовые продукты (удаляя старые данные)"

    def handle(self, *args, **kwargs):
        # 1. Удаляем все существующие данные
        self.stdout.write("Удаление существующих данных...")
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✓ Все данные удалены"))

        # 2. Создаём категории
        self.stdout.write("Создание категорий...")
        electronics = Category.objects.create(name="Электроника")
        books = Category.objects.create(name="Книги")
        clothes = Category.objects.create(name="Одежда")
        self.stdout.write(self.style.SUCCESS("✓ Создано 3 категории"))

        # 3. Создаём продукты
        self.stdout.write("Создание продуктов...")
        products_data = [
            {
                "name": "Ноутбук",
                "price": 60000,
                "category": electronics,
                "description": "Мощный ноутбук для работы",
            },
            {
                "name": "Смартфон",
                "price": 30000,
                "category": electronics,
                "description": "Современный смартфон с отличной камерой",
            },
            {
                "name": "Наушники",
                "price": 5000,
                "category": electronics,
                "description": "Беспроводные наушники",
            },
            {
                "name": "Python для начинающих",
                "price": 1500,
                "category": books,
                "description": "Книга по Python",
            },
            {
                "name": "Django для профи",
                "price": 2000,
                "category": books,
                "description": "Продвинутый Django",
            },
            {
                "name": "Футболка",
                "price": 1200,
                "category": clothes,
                "description": "Хлопковая футболка",
            },
            {
                "name": "Джинсы",
                "price": 3500,
                "category": clothes,
                "description": "Удобные джинсы",
            },
        ]

        for product in products_data:
            Product.objects.create(
                name=product["name"],
                price=product["price"],
                category=product["category"],
                description=product["description"],
            )
        self.stdout.write(
            self.style.SUCCESS(f"✓ Создано {len(products_data)} продуктов")
        )

        # 4. Вывод итогов
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("ГОТОВО!"))
        self.stdout.write(f"Категорий: {Category.objects.count()}")
        self.stdout.write(f"Продуктов: {Product.objects.count()}")
        self.stdout.write("=" * 50)
