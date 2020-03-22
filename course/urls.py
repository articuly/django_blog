from django.urls import path
from django.views.generic import TemplateView
from .views import CourseHome

app_name = 'course'

urlpatterns = [
    path('', CourseHome.as_view()),
]
