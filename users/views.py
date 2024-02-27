from django.shortcuts import redirect, render
from django.views import View
from users.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import User
from django.contrib.auth import update_session_auth_hash
from .forms import UserChangeForm

def open_admin(request):
    return redirect('admin:index')

# Create your views here.
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)  
            login(request, user)
            return redirect('login')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


""" @method_decorator(login_required(login_url='login'), name='dispatch')
class EditProfileView(View):
    template_name = 'registration/profile.html'
    form_class = CustomUserChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля после успешного редактирования
        return render(request, self.template_name, {'form': form})
 """

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditProfileView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')  # Перенаправление на страницу профиля после успешного обновления

    def get_object(self, queryset=None):
        return self.request.user  # Получение текущего зарегистрированного пользователя в качестве обновляемого объекта

    def form_valid(self, form):
        # Сохраните обновленный экземпляр пользователя и обновите сессию
        user = form.save()
        update_session_auth_hash(self.request, user)  # Обновление сессии для предотвращения выхода из нее после смены пароля
        return super().form_valid(form)
