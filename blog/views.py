from django.shortcuts import render
from .models import BlogArticles


def blog_home(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blog/home.html', {'blogs': blogs})


def blog_article(request, article_id):
    article = BlogArticles.objects.get(id=article_id)
    pub = article.publish
    return render(request, 'blog/article.html', {'article': article, 'publish': pub})
