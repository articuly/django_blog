from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Course


class CourseHome(TemplateView):
    template_name = 'course/home.html'


class CourseListView(ListView):
    model = Course  # Course.objects.all()
    template_name = 'course/course_list.html'
    context_object_name = 'course'
