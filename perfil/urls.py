from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('login/', views.Login.as_view(), name='login'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('passwordreset/', views.PasswordReset.as_view(), name='passwordreset'),
    path('novasenha/', views.PasswordForgot.as_view(), name='novasenha')

]
