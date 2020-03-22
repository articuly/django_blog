from django.urls import path
from .views import CourseHome, CourseListView

app_name = 'course'

urlpatterns = [
    path('', CourseHome.as_view()),
    path('course-list', CourseListView.as_view(), name='course_list')
]
