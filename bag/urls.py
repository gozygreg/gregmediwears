from django.urls import path
from . import views


urlpatterns = [
    path('', views.bag_summary, name='bag-summary'),
    path('add/', views.bag_add, name='bag-add'),
    path('delete/', views.bag_delete, name='bag-delete'),
    path('update/', views.bag_update, name='bag-update'),
]