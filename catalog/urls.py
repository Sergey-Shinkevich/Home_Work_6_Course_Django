from django.urls import path
from django.views.decorators.cache import cache_page
from .views import ContactsView, HomeView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView, ProductByCategoryListView

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", cache_page(60 * 15)(ProductDetailView.as_view()), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("category/<int:category_id>/products/", ProductByCategoryListView.as_view(), name="products_by_category"),
]
