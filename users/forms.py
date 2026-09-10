from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


# Форма регистрации
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        # Автоматически дублируем email в поле username, чтобы избежать конфликтов уникальности
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# Форма авторизации
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
