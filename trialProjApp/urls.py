from django.urls import path

from . import views

app_name = 'trial_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    # path('download/', views.download_csv, name='downloadCSV'),
    path('<str:meter_id>/', views.detail, name='detail'),
    path('<str:meter_id>/deleteAll/', views.delete_all, name='deleteAll'),
    path('<str:meter_id>/uploadData/', views.upload_data, name='uploadData'),
    path('<str:meter_id>/download/', views.download_csv, name='downloadCSV'),
]
