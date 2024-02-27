from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
User = get_user_model()
from .models import User

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User  # Используйте вашу модель пользователя здесь
        fields = ('username', 'email', 'password',)  # Укажите поля, которые вы хотите редактировать
