from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from catalog.services import get_products_by_category


from .forms import ProductForm
from .models import Product, Category


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "object_list"


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        # Привязываем продукт к текущему пользователю перед сохранением
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        # Проверяем, что текущий пользователь является владельцем продукта
        return user == product.owner or self.request.user.has_perm("catalog.can_unpublish_product")


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or self.request.user.has_perm("catalog.delete_product")


class ProductByCategoryListView(ListView):
    model = Product
    template_name = "product_by_category.html"
    context_object_name = "product_list"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.get("category_id"))
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем саму категорию в контекст, чтобы вывести её название в шаблоне
        context["category"] = self.category
        return context
