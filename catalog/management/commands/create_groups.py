from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = "Создание группы 'Модератор продуктов' и назначение ей прав доступа"

    def handle(self, *args, **options):
        # 1. Создаем или получаем группу
        moderator_group, created = Group.objects.get_or_create(name="Модератор продуктов")
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует. Обновляем права...'))

        # 2. Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        # 3. Собираем кодовые имена прав, которые нужно назначить: кастомное право на отмену публикации,
        # - встроенное право на удаление продукта (Django создает его автоматически: delete_<model_name>)
        permission_codenames = [
            "can_unpublish_product",
            f"delete_{Product._meta.model_name}",
        ]

        # 4. Находим эти разрешения в базе данных
        permissions = Permission.objects.filter(content_type=product_content_type, codename__in=permission_codenames)

        # 5. Назначаем найденные права группе
        moderator_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Права успешно назначены группе 'Модератор продуктов'."))
