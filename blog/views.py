from django.shortcuts import render
from .models import BlogArticles
from django.contrib.auth.decorators import login_required
from .forms import BlogArticlesForm
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def blog_home(request):
    blogs = BlogArticles.objects.all()
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')  # http://localhost:8000/blog/?page=1
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    current_blogs = current_page.object_list
    return render(request, 'blog/home.html', {'blogs': current_blogs, 'page': current_page})


def blog_article(request, article_id):
    article = BlogArticles.objects.get(id=article_id)
    pub = article.publish
    return render(request, 'blog/article.html', {'article': article, 'publish': pub})


@login_required
def blog_post(request):
    if request.method == 'GET':
        blog_form = BlogArticlesForm()
        return render(request, 'blog/post.html', {'blog_form': blog_form})
    if request.method == 'POST':
        blog_form = BlogArticlesForm(request.POST)
        if blog_form.is_valid():
            cd = blog_form.cleaned_data
            try:
                blog = blog_form.save(commit=False)
                blog.author = request.user
                blog.save()
                return HttpResponse('1')
            except:
                return HttpResponse('-1')
        else:
            return HttpResponse('0')
