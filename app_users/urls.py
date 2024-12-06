from django.urls import path
from django.contrib.auth.views import LoginView

from app_users import views

urlpatterns = [
    path('account/<int:user_id>/', views.AccountView.as_view(), name='account'),
    # Auth
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
