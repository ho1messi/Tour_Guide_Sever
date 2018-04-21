from django.urls import path
from . import views

urlpatterns = [
    path('scenic_areas/', views.scenic_areas, name='scenic_areas'),
]