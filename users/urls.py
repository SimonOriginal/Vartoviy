from django.urls import include, path
from users.views import Register, EditProfileView
from .views import open_admin


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('open_admin/', open_admin, name='open_admin'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', EditProfileView.as_view(), name='profile'),

]