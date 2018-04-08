from django.urls import path
from . import views

urlpatterns = [
    path('article/', views.article_view, name='article'),
    path('comment/', views.comment_view, name='comment'),
    path('check_login/', views.have_logined, name='check login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]