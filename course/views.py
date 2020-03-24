from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Course
from braces.views import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect
from .forms import CourseCreateForm
from django.urls import reverse_lazy
from django.http import HttpResponse
import json


class CourseHome(TemplateView):
    template_name = 'course/home.html'


class UserMixin:  # 筛选用户的类
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):  # 操作的模型
    model = Course
    login_url = '/account/login/'


class CourseListView(UserCourseMixin, ListView):  # 多重继承
    # model = Course  # Course.objects.all()
    template_name = 'course/course_list.html'
    context_object_name = 'courses'  # 前端模板变量名


class CourseCreateView(UserCourseMixin, CreateView):
    fields = ['title', 'overview', 'video', 'attach']
    template_name = 'course/course_create.html'

    def post(self, request, *args, **kwargs):
        form = CourseCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect('course:course_list')
        return self.render_to_response({'form': form})


class CourseDeleteView(UserCourseMixin, DeleteView):
    success_url = reverse_lazy('course:course_list')

    def dispatch(self, *args, **kwargs):  # 重写方法，适应AJAX提交
        resp = DeleteView.dispatch(self, *args, **kwargs)
        if self.request.is_ajax():
            response_data = {'result': 'OK'}  # 是AJAX提交，用json返回OK
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return resp  # 非AJAX提交直接返回


class CourseDetailView(UserCourseMixin, DetailView):
    pass
