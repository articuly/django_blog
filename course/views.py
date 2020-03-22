from django.shortcuts import render
from django.views.generic import TemplateView


class CourseHome(TemplateView):
    template_name = 'course/home.html'
