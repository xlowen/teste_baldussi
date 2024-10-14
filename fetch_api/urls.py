from django.urls import path
from . import views

urlpatterns =[
    path('', views.principal, name='home'),
    path('povoardb', views.fetch_api_users, name='fetch_data'),
    path('listar', views.listar_todos, name='listar_todos')
    ]