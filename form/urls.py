from django.urls import path
from . import views

urlpatterns = [
    path(r'detail/article/<int:article_id>/', views.article_detail, name='article_detail'),
    path(r'detail/discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('article_list/', views.article_list, name='article'),
    path('discussion_list/', views.discussion_list, name='discussion'),
    path('check_login/', views.have_logined, name='check login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]