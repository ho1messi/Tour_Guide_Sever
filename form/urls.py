from django.urls import path
from . import views

urlpatterns = [
    path('detail/article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('detail/discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('area/article_list/<int:area_id>/', views.area_article_list, name='area_article_list'),
    path('area/discussion_list/<int:area_id>/', views.area_discussion_list, name='area_discussion_list'),
    path('spot/article_list/<int:spot_id>/', views.spot_article_list, name='spot_article_list'),
    path('spot/discussion_list/<int:spot_id>/', views.spot_discussion_list, name='spot_discussion_list'),
    path('article_list/', views.article_list, name='article_list'),
    path('discussion_list/', views.discussion_list, name='discussion_list'),
    path('check_login/', views.have_logined, name='check login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]