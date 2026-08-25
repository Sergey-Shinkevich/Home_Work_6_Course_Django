from django.urls import reverse_lazy
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

  def get_queryset(self, *args, **kwargs):
    # Опционально: выводим только те статьи, которые опубликованы
    queryset = super().get_queryset(*args, **kwargs)
    queryset = queryset.filter(is_published=True)
    return queryset


class BlogDetailView(DetailView):
  model = BlogPost
  template_name = 'blog/blog_detail.html'

  def get_object(self, queryset=None):
    # Увеличиваем счетчик просмотров при каждом открытии статьи
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

  def get_success_url(self):
    return reverse_lazy('blog:view', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
  model = BlogPost
  template_name = 'blog/blog_confirm_delete.html'
  success_url = reverse_lazy('blog:list')
