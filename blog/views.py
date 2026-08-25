from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import BlogPost


class BlogListView(ListView):
  model = BlogPost
  template_name = 'blog/blog_list.html'

  # 1. Фильтрация опубликованных статей (выводим только те, у которых is_published=True)
  def get_queryset(self, *args, **kwargs):
    queryset = super().get_queryset(*args, **kwargs)
    queryset = queryset.filter(is_published=True)
    return queryset


class BlogDetailView(DetailView):
  model = BlogPost
  template_name = 'blog/blog_detail.html'

  # 2. Увеличение счетчика просмотров при открытии отдельной статьи
  def get_object(self, queryset=None):
    self.object = super().get_object(queryset)
    self.object.views_count += 1
    self.object.save()
    return self.object


class BlogCreateView(CreateView):
  model = BlogPost
  template_name = 'blog/blog_form.html'
  fields = ('title', 'content', 'preview', 'is_published')
  success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
  model = BlogPost
  template_name = 'blog/blog_form.html'
  fields = ('title', 'content', 'preview', 'is_published')

  # 3. Перенаправление после успешного редактирования на просмотр этой же статьи
  def get_success_url(self):
    return reverse('blog:view', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
  model = BlogPost
  template_name = 'blog/blog_confirm_delete.html'
  success_url = reverse_lazy('blog:list')