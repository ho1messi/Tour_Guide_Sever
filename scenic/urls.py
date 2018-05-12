from django.urls import path
from . import views

urlpatterns = [
    path('detail/area/<int:area_id>/', views.area_detail, name='area_detail'),
    path('detail/spot/<int:spot_id>/', views.spot_detail, name='spot_detail'),
    path('detail/area_and_spot/<int:spot_id>/', views.area_and_spot, name='area_and_spot'),
    path('area_list/', views.area_list, name='area_list'),
    path('spot_list/<int:area_id>', views.spot_list, name='spot_list'),
    path('upload_image/', views.upload_image, name='upload_image'),
]