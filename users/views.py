from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from users.models import CustomUser

class RegisterView(CreateView):
    model = CustomUser
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')


    def form_valid(self, form):
        # Сохраняем пользователя в БД
        response = super().form_valid(form)
        user = self.object

        # <--- Автоматически авторизуем пользователя
        login(self.request, user)

        # Формируем и отправляем письмо
        send_mail(
            subject='Добро пожаловать!',
            message=f'Здравствуйте, {user.email}!\n\nСпасибо за регистрацию на нашем сайте.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,  # Вызовет ошибку, если письмо не отправится
        )

        return response
