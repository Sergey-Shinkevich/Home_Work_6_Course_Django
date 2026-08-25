from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок", help_text="Введите заголовок")
    slug = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog/preview",
        blank=True,
        null=True,
        verbose_name="Превью (изображение)",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
