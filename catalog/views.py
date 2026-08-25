from django.shortcuts import get_object_or_404, render
from .models import Product

def home(request):
    products = Product.objects.all()
    context = {'object_list': products}
    return render(request, "home.html", context=context)


def contacts(request):
    return render(request, "contacts.html")

def product_detail_view(request, pk):
  # Достаем товар по id или выдаем 404 ошибку, если его нет
  product = get_object_or_404(Product, pk=pk)
  context = {
      'product': product,
  }
  return render(request, 'product_detail.html', context)