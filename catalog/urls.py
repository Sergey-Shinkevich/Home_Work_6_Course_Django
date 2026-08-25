from django.urls import include, path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_detail_view

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path('product/<int:pk>/', product_detail_view, name='product_detail'),
]
