import json

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Очищает базу и загружает данные из фикстуры"

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING("База очищена."))

        # Загрузка данных из фикстуры
        try:
            call_command("loaddata", "catalog/fixtures/catalog_fixture.json")
            self.stdout.write(self.style.SUCCESS("Данные из фикстуры успешно загружены!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке фикстуры: {e}"))
