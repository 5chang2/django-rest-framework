from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_create),
    path('<int:id>/', views.read_update_delete),
]