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
    path('article/comment_list/<int:article_id>/', views.article_comment_list, name='article_comment_list'),
    path('discussion/comment_list/<int:discussion_id>/', views.discussion_comment_list, name='discussion_comment_list'),
    path('publish/article/', views.publish_article, name='publish_article'),
    path('publish/discussion/', views.publish_discussion, name='publish_discussion'),
    path('publish/comment/', views.publish_comment, name='publish_comment'),
    path('publish/vote/', views.publish_vote, name='publish_vote'),
    path('check_login/', views.have_logined, name='check login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]