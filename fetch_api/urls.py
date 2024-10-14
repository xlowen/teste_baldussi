from django.urls import path
from . import views

urlpatterns =[
    path('', views.principal, name='home'),
    path('povoardb', views.fetch_api_users, name='fetch_data'),
    path('listar', views.listar_todos, name='listar_todos'),
    path('usuarios/genero/<str:gender>/',views.get_users_by_gender, name='usuarios_por_genero'),
    path('usuarios/idade/<int:age>/',views.get_users_by_age, name='usuarios_por_idade'),
    ]