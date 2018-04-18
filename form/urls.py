from django.urls import path
from . import views

urlpatterns = [
    path(r'detail/article/<int:article_id>/', views.article_detail, name='article_detail'),
    path(r'detail/comment/<int:article_id>/', views.comment_detail, name='comment_detail'),
    path('article/', views.article_view, name='article'),
    path('comment/', views.comment_view, name='comment'),
    path('check_login/', views.have_logined, name='check login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]