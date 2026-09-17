from django.conf import settings
from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """Возвращает список продуктов для указанной категории с учетом флага CACHE_ENABLED из настроек."""
    cache_key = f"category_{category_id}"

    # 1. Проверяем, включен ли кэш в настройках
    if getattr(settings, "CACHE_ENABLED", False):
        # Пытаемся достать данные из кэша
        products = cache.get(cache_key)
        if products is not None:
            return products

    # 2. Если кэш отключен ИЛИ в кэше пусто (None) — идем в базу данных
    products = list(Product.objects.filter(category_id=category_id))

    # 3. Если кэш включен, сохраняем свежие данные в кэш на 15 минут)
    if getattr(settings, "CACHE_ENABLED", False):
        cache.set(cache_key, products, 60 * 15)

    return products