from django.urls import path
from .views import CourseHome, CourseListView, CourseCreateView, CourseDeleteView

app_name = 'course'

urlpatterns = [
    path('', CourseHome.as_view()),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('delete/<int:pk>', CourseDeleteView.as_view(), name='course_delete'),  # pk为通用类定义的变量
]
