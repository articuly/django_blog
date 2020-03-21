from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('<int:article_id>/', views.blog_article, name='blog_article')
]
