from catalog.models import Product


def get_products_by_category(category_id):
    """Возвращает список всех продуктов для указанной категории."""
    return Product.objects.filter(category_id=category_id)