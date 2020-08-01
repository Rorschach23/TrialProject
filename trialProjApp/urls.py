from django.urls import path

from . import views

app_name = 'trial_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<str:meter_id>/', views.detail, name='detail'),
    path('<str:meter_id>/deleteAll/', views.deleteAll, name='deleteAll'),
    path('<str:meter_id>/uploadData/', views.uploadData, name='uploadData')

]